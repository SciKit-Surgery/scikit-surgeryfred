"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

class PlotRegStatistics():
    """
    writes the registration statistics
    """
    def __init__(self, plot):
        """
        The plot to write on
        """
        self.plot = plot

        self.texts = {
            'fids_text' : None,
            'tre_text' : None,
            'exp_tre_text' : None,
            'exp_fre_text' : None,
            'fre_text' : None,
            'score_text' : None,
            'total_score_text' : None,
            'margin_text' : None,
            'repeats_text' : None
            }

        self.visibilities = {
            'fids_text' : False,
            'tre_text' : False,
            'exp_tre_text' : False,
            'exp_fre_text' : False,
            'fre_text' : False,
            'score_text' : False,
            'total_score_text' : False,
            'margin_text' : False,
            'repeats_text' : False
            }

        self.props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)

    def set_visibilities(self,
                         fids_text, tre_text, exp_tre_text, exp_fre_text,
                         fre_text,
                         score_text, total_score_text, margin_text,
                         repeats_text):
        """
        Sets which text boxes will be visible
        """
        self.visibilities = {
            'fids_text' : fids_text,
            'tre_text' : tre_text,
            'exp_tre_text' : exp_tre_text,
            'exp_fre_text' : exp_fre_text,
            'fre_text' : fre_text,
            'score_text' : score_text,
            'total_score_text' : total_score_text,
            'margin_text' : margin_text,
            'repeats_text' : repeats_text
            }


    def update_stats_plot(self, tre, exp_tre, fre, exp_fre):
        """
        Updates the statistics display
        """
        if self.texts.get('tre_text') is not None:
            try:
                self.texts.get('tre_text').remove()
            except ValueError:
                pass
        if self.texts.get('exp_tre_text') is not None:
            try:
                self.texts.get('exp_tre_text').remove()
            except ValueError:
                pass
        if self.texts.get('fre_text') is not None:
            try:
                self.texts.get('fre_text').remove()
            except ValueError:
                pass

        exp_tre_str = ('Expected TRE = {0:.2f}'.format(exp_tre))
        exp_fre_str = ('Expected FRE = {0:.2f}\n'.format(exp_fre))
        stats_str = ''

        if self.visibilities.get('exp_fre_text'):
            stats_str += exp_fre_str

        if self.visibilities.get('exp_tre_text'):
            stats_str += exp_tre_str

        actual_tre_str = ('Actual TRE = {0:.2f}'.format(tre))
        actual_fre_str = ('Actual FRE = {0:.2f}'.format(fre))

        if (self.visibilities.get('exp_tre_text') or
                self.visibilities.get('exp_fre_text')):
            self.texts['exp_tre_text'] = self.plot.text(
                -0.90, 1.10, stats_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)


        if self.visibilities.get('tre_text'):
            self.texts['tre_text'] = self.plot.text(
                -0.05, 1.10, actual_tre_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)

        if self.visibilities.get('fre_text'):
            self.texts['fre_text'] = self.plot.text(
                0.65, 1.10, actual_fre_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)


    def update_fids_stats(self, no_fids, mean_fle):
        """
        Updates the fids stats display
        """
        if self.texts.get('fids_text') is not None:
            try:
                self.texts.get('fids_text').remove()
            except ValueError:
                pass

        fids_str = ('Number of fids = {0:}\n'.format(no_fids) +
                    'Expected FLE = {0:.2f}'.format(mean_fle))

        if self.visibilities.get('fids_text'):
            self.texts['fids_text'] = self.plot.text(
                -1.65, 1.10, fids_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)

    def update_margin_stats(self, margin):
        """
        Updates the margin text box
        """
        if self.texts.get('margin_text') is not None:
            self.texts.get('margin_text').remove()

        fids_str = ('Margin: {0:.1f}'.format(margin))

        if self.visibilities.get('margin_text'):
            self.texts['margin_text'] = self.plot.text(
                1.05, 0.5, fids_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)

    def update_last_score(self, last_score):
        """
        Updates the margin text box
        """
        if self.texts.get('score_text') is not None:
            self.texts.get('score_text').remove()

        fids_str = ('Last Score\n{0:}'.format(last_score))
        if self.visibilities.get('score_text'):
            self.texts['score_text'] = self.plot.text(
                1.05, 0.7, fids_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)

    def update_total_score(self, total_score):
        """
        Updates the total score text box
        """
        if self.texts.get('total_score_text') is not None:
            self.texts.get('total_score_text').remove()

        fids_str = ('Total Score\n{0:}'.format(total_score))

        if self.visibilities.get('total_score_text'):
            self.texts['total_score_text'] = self.plot.text(
                1.05, 0.9, fids_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)

    def update_repeats(self, repeats):
        """
        Updates the total score text box
        """
        if self.texts.get('repeats_text') is not None:
            self.texts.get('repeats_text').remove()

        fids_str = ('Reps:{0:}'.format(repeats))

        if self.visibilities.get('repeats_text'):
            self.texts['repeats_text'] = self.plot.text(
                1.05, 0.3, fids_str, transform=self.plot.transAxes,
                fontsize=26, verticalalignment='top', bbox=self.props)


class PlotRegistrations():
    """
    Plots the results of registrations
    """

    def __init__(self, fixed_plot, moving_plot, stats_plot):
        """
        :params fixed_plot: the fixed image subplot
        :params moving_plot: the moving image subplot
        """

        self.fixed_plot = fixed_plot
        self.moving_plot = moving_plot

        self.target_scatter = None
        self.trans_target_plots = [None, None]
        self.fixed_fids_plots = [None, None]
        self.moving_fids_plot = None

        self.stats_plot = stats_plot

        self.show_actual_positions = True
        self.target_point = None

    def initialise_new_reg(self, img, target_point, outline):
        """
        resets the registration
        """
        self.moving_plot.imshow(img)
        self.fixed_plot.plot(outline[:, 1], outline[:, 0], '-b', lw=3)
        self.fixed_plot.set_ylim([0, img.shape[0]])
        self.fixed_plot.set_xlim([0, img.shape[1]])
        self.fixed_plot.axis([0, img.shape[1], img.shape[0], 0])
        self.fixed_plot.axis('scaled')
        self.target_point = target_point

        if self.target_scatter is not None:
            self.target_scatter.remove()

        self.target_scatter = self.moving_plot.scatter(self.target_point[0, 0],
                                                       self.target_point[0, 1],
                                                       s=144, c='r')
        if self.trans_target_plots[0] is not None:
            self.trans_target_plots[0].remove()
            self.trans_target_plots[0] = None

        if self.trans_target_plots[1] is not None:
            self.trans_target_plots[1].remove()
            self.trans_target_plots[1] = None

        self.stats_plot.update_stats_plot(0, 0, 0, 0)

        self.moving_plot.set_title('Pre-Operative Image', y=-0.10,
                                   fontsize=26)
        self.fixed_plot.set_title('Patient in Theatre', y=-0.10,
                                  fontsize=26)


    def plot_fiducials(self, fixed_points, moving_points, no_fids, mean_fle):
        """
        Updates plot with fiducial data
        """

        if self.fixed_fids_plots[0] is not None:
            self.fixed_fids_plots[0].remove()
        if self.moving_fids_plot is not None:
            self.moving_fids_plot.remove()

        if self.fixed_fids_plots[1] is not None:
            self.fixed_fids_plots[1].remove()


        self.fixed_fids_plots[0] = self.fixed_plot.scatter(fixed_points[:, 0],
                                                           fixed_points[:, 1],
                                                           s=64, c='g',
                                                           marker='o')
        self.moving_fids_plot = self.moving_plot.scatter(moving_points[:, 0],
                                                         moving_points[:, 1],
                                                         s=64, c='g',
                                                         marker="o")

        if self.show_actual_positions:
            self.fixed_fids_plots[1] = self.fixed_plot.scatter(
                moving_points[:, 0],
                moving_points[:, 1],
                s=36, c='black',
                marker='+')

        self.stats_plot.update_fids_stats(no_fids, mean_fle)

    def plot_registration_result(self, actual_tre, expected_tre,
                                 fre, expected_fre, transformed_target_2d):
        """
        Plots the results of a registration
        """

        self.stats_plot.update_stats_plot(actual_tre, expected_tre,
                                          fre, expected_fre)


        if self.trans_target_plots[0] is not None:
            self.trans_target_plots[0].remove()

        if self.trans_target_plots[1] is not None:
            self.trans_target_plots[1].remove()

        self.trans_target_plots[0] = self.fixed_plot.scatter(
            transformed_target_2d[0],
            transformed_target_2d[1],
            s=144, c='r', marker='o')

        if self.show_actual_positions:
            self.trans_target_plots[1] = self.fixed_plot.scatter(
                self.target_point[0, 0],
                self.target_point[0, 1],
                s=36, c='black', marker='+')
