"""
The main widget for the interactive registration part of scikit-surgeryFRED
"""

# pylint: disable=raise-missing-from

from random import shuffle
import matplotlib.pyplot as plt
from matplotlib import use
import skimage.io
import numpy as np

from sksurgeryfred.algorithms.fred import make_target_point, \
                AddFiducialMarker
from sksurgeryfred.plotting.interactive_plots import PlotRegistrations, \
                PlotRegStatistics
from sksurgeryfred.algorithms.point_based_reg import PointBasedRegistration
from sksurgeryfred.algorithms.fit_contour import find_outer_contour
from sksurgeryfred.algorithms.errors import expected_absolute_value
from sksurgeryfred.algorithms.ablation import Ablator
from sksurgeryfred.logging.fred_logger import Logger

class RegistrationGame:
    """
    an interactive window for doing live registration
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, image_file_name):
        """
        Creates a visualisation of the projected and
        detected screen points, which you can click on
        to measure distances
        """
        use('TkAgg')
        self.fig, subplot = plt.subplots(1, 2, figsize=(20, 10))
        self.fig.canvas.set_window_title('SciKit-SurgeryF.R.E.D.')
        self.stats_plot = PlotRegStatistics(subplot[1])
        self.stats_plot.set_visibilities(True, True, False, False, False,
                                         True, True, True, True)
        self.state_string = 'Actual TRE'
        self.repeats = 20
        self.visibility_setter = VisibilitySettings(self.repeats - 4)
        self.total_score = 0
        self.stats_plot.update_last_score(0)
        self.stats_plot.update_total_score(self.total_score)

        self.plotter = PlotRegistrations(subplot[1], subplot[0],
                                         self.stats_plot)

        self.plotter.show_actual_positions = False

        log_config = {"logger" : {
            "log file name" : "fred_game.log",
            "overwrite existing" : False
            }}

        self.logger = Logger(log_config)
        self.mouse_int = None
        self.pbr = None
        self.image_file_name = image_file_name
        self.ablation = Ablator(margin=1.0)

        self.intialise_registration()

        _ = self.fig.canvas.mpl_connect('key_press_event',
                                        self.keypress_event)

        plt.show()

    def keypress_event(self, event):
        """
        handle a key press event
        """

        if event.key == "up":
            margin = self.ablation.increase_margin()
            self.stats_plot.update_margin_stats(margin)
            self.fig.canvas.draw()

        if event.key == "down":
            margin = self.ablation.decrease_margin()
            self.stats_plot.update_margin_stats(margin)
            self.fig.canvas.draw()

        if event.key == "a":
            reg_ok, est_target = self.pbr.get_transformed_target()
            if reg_ok:
                score = self.ablation.ablate(est_target)
                if score is not None:
                    self.stats_plot.update_last_score(score)
                    self.total_score += score
                    self.stats_plot.update_total_score(self.total_score)
                    self.logger.log_score(self.state_string, score)
                    if self.repeats > 1:
                        if self.repeats < 18:
                            [fids_text, tre_text, exp_tre_text, exp_fre_text,
                             fre_text, score_text, total_score_text,
                             margin_text, repeats_text, self.state_string] = \
                                 self.visibility_setter.get_vis_state()
                            self.stats_plot.set_visibilities(
                                fids_text, tre_text, exp_tre_text, exp_fre_text,
                                fre_text, score_text, total_score_text,
                                margin_text, repeats_text)
                        self.repeats -= 1
                        self.stats_plot.update_repeats(self.repeats)
                        self.intialise_registration()
                    else:
                        self._game_over()
                    self.fig.canvas.draw()

    def _game_over(self):
        props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
        self.fig.text(0.2, 0.7, "Game Over",
                      fontsize=56, bbox=props)

        text_str = ("Thanks for playing.\n" +
                    "Please let me know your scores by sending the log file\n" +
                    "'fred_game.log' and any comments to s.thompson@ucl.ac.uk")
        self.fig.text(0.2, 0.4, text_str,
                      fontsize=26, bbox=props)

        self.fig.canvas.draw()

    def intialise_registration(self):
        """
        sets up the registration
        """
        img = skimage.io.imread(self.image_file_name)
        outline, _initial_guess = find_outer_contour(img)
        target_point = make_target_point(outline)

        self.plotter.initialise_new_reg(img, target_point, outline)

        fle_sd = np.random.uniform(low=0.5, high=5.0)
        moving_fle = np.zeros((1, 3), dtype=np.float64)

        fixed_fle = np.array([fle_sd, fle_sd, fle_sd], dtype=np.float64)
        fixed_fle_eavs = expected_absolute_value(fixed_fle)
        moving_fle_eavs = expected_absolute_value(moving_fle)

        if self.pbr is None:
            self.pbr = PointBasedRegistration(target_point, fixed_fle_eavs,
                                              moving_fle_eavs)
        else:
            self.pbr.reinit(target_point, fixed_fle_eavs, moving_fle_eavs)

        if self.mouse_int is None:
            self.mouse_int = AddFiducialMarker(self.fig, self.plotter,
                                               self.pbr, None,
                                               fixed_fle, moving_fle,
                                               max_fids=6)

        self.mouse_int.reset_fiducials(fixed_fle_eavs)

        self.ablation.setup(target=target_point,
                            target_radius=10.0)

        self.stats_plot.update_margin_stats(self.ablation.margin)
        self.stats_plot.update_repeats(self.repeats)

        self.fig.canvas.draw()


class VisibilitySettings:
    """
    randomly selects from list of visilities, has five states
    FLE and no fids
    Expected FRE
    Expected TRE
    Actual FRE
    """
    def __init__(self, buffer_size):
        """
        :params buffer_size: the number of repeats you want, should be a
            product of 4
        """
        if buffer_size % 4 != 0:
            raise ValueError("Buffer size must be divisible by 4")

        each_bin = int(buffer_size / 4)

        fle_and_fids = [True, False, False, False, False,
                        True, True, True, True, 'FLE and Number of Fids']
        exp_tre = [False, False, True, False, False, True, True, True, True,
                   'Expected TRE']
        exp_fre = [False, False, False, True, False, True, True, True, True,
                   'Expected FRE']
        actual_fre = [False, False, False, False, True, True, True, True, True,
                      'Actual FRE']

        self.state_list = []

        for _ in range(each_bin):
            self.state_list.append(fle_and_fids)
            self.state_list.append(exp_tre)
            self.state_list.append(exp_fre)
            self.state_list.append(actual_fre)

    def get_vis_state(self):
        """
        returns a random visibility state
        """
        shuffle(self.state_list)
        try:
            return self.state_list.pop()
        except IndexError:
            raise IndexError("You tried to get a value from" +
                             "VisibilitySettings, but the buffer is emptied.")
