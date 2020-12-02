"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import math
import numpy as np

from sksurgeryfredbe.algorithms.fle import FLE

class AddFiducialMarker:
    """
    A class to handle mouse press events, adding a fiducial
    marker.
    """

    def __init__(self, fig, plotter,
                 pbr, logger, fixed_fle_sd, moving_fle_sd,
                 max_fids=None):
        """
        :params fig: the matplot lib figure to get mouse events from
        :params fixed_plot: the fixed image subplot
        :params moving_plot: the moving image subplot
        :params target: 1x3 target point
        :params fixed_fle: the standard deviations of the fixed image fle
        :params moving_fle: the standard deviations of the moving image fle
        """

        self.pbr = pbr
        self.plotter = plotter
        self.fig = fig
        _ = fig.canvas.mpl_connect('button_press_event', self)
        self.logger = logger
        self.fixed_points = None
        self.moving_points = None
        self.fids_plot = None
        self.fixed_fle = FLE(independent_fle=fixed_fle_sd.reshape(3))
        self.moving_fle = FLE(independent_fle=moving_fle_sd.reshape(3))
        self.max_fids = max_fids

        self.reset_fiducials(0.0)

    def __call__(self, event):
        if event.xdata is not None:
            fiducial_location = np.zeros((3), dtype=np.float64)
            fiducial_location[0] = event.xdata
            fiducial_location[1] = event.ydata

            if self.max_fids is not None:
                if self.fixed_points.shape[0] >= self.max_fids:
                    return

            if _is_valid_fiducial(fiducial_location):
                fixed_point = self.fixed_fle.perturb_fiducial(fiducial_location)
                moving_point = self.moving_fle.perturb_fiducial(
                    fiducial_location)
                self.fixed_points = np.concatenate(
                    (self.fixed_points, fixed_point.reshape(1, 3)), axis=0)
                self.moving_points = np.concatenate(
                    (self.moving_points, moving_point.reshape(1, 3)), axis=0)

                [success, fre, mean_fle_sq, expected_tre_sq,
                 expected_fre_sq, transformed_target_2d,
                 actual_tre, no_fids] = self.pbr.register(
                     self.fixed_points, self.moving_points)

                mean_fle = math.sqrt(mean_fle_sq)
                self.plotter.plot_fiducials(self.fixed_points,
                                            self.moving_points,
                                            no_fids,
                                            mean_fle)

                if success:
                    expected_tre = math.sqrt(expected_tre_sq)
                    expected_fre = math.sqrt(expected_fre_sq)
                    self.plotter.plot_registration_result(
                        actual_tre, expected_tre,
                        fre, expected_fre, transformed_target_2d)
                    if self.logger is not None:
                        self.logger.log_result(
                            actual_tre, fre, expected_tre, expected_fre,
                            mean_fle, no_fids)
                self.fig.canvas.draw()

    def reset_fiducials(self, mean_fle_sq):
        """
        resets the fiducial markers
        """
        self.fixed_points = np.zeros((0, 3), dtype=np.float64)
        self.moving_points = np.zeros((0, 3), dtype=np.float64)
        self.plotter.plot_fiducials(self.fixed_points,
                                    self.moving_points,
                                    0, math.sqrt(mean_fle_sq))


def _is_valid_fiducial(_unused_fiducial_location):
    """
    Checks the x, y, and z location of a fiducial
    :returns: true if a valid fiducial
    """
    return True

def make_target_point(outline, edge_buffer=0.9):
    """
    returns a target point, that should lie
    within the outline.
    """
    #let's assume the anatomy is a circle with
    #centre, and radius
    centre = np.mean(outline, 0)
    max_radius = np.min((np.max(outline, 0) - np.min(outline, 0))/2)*edge_buffer
    radius = np.random.uniform(low=0.0, high=max_radius)
    radius = np.random.uniform(low=0.0, high=max_radius)
    angle = np.random.uniform(low=0.0, high=math.pi*2.0)
    x_ord = radius * math.cos(angle) + centre[0]
    y_ord = radius * math.sin(angle) + centre[1]
    return np.array([[x_ord, y_ord, 0.0]])
