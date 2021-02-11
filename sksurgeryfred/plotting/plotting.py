"""Plotting functions for scikit-surgeryFRED
"""

import matplotlib.pyplot as plt
from matplotlib import use
from numpy import polyfit, corrcoef, array

from sksurgeryfred.logging.fred_logger import Logger

def _plot_subresults(subplot, x_values, y_values):
    """
    scatter plot, fitted line, and correlation coefficient
    """
    subplot.scatter(x_values, y_values)
    slope, intercept = polyfit(array(x_values), array(y_values), 1)
    correl_coeff = corrcoef(array(x_values), array(y_values))[0, 1]
    subplot.set_title("Corr. Coef. = {0:.3f}".format(correl_coeff), fontsize=16)
    subplot.plot(x_values, intercept + slope * array(x_values), '-')


def plot_results(logfile):
    """
    Plots the results  of multiple runs, from the log file.
    """

    log_config = {"logger" : {
        "log file name" : logfile,
        "overwrite existing" : False
        }}

    logger = Logger(log_config)

    [actual_tres, actual_fres, expected_tres, expected_fres,
     mean_fles, no_fids] = logger.read_log()

    use('TkAgg')
    fig, subplot = plt.subplots(1, 5, figsize=(18, 8))

    fig.canvas.set_window_title('SciKit-SurgeryF.R.E.D. Correlation Plots')

    subplot[0].set_ylabel("TRE", fontsize=26)
    subplot[0].set_xlabel("Actual FRE", fontsize=26)
    _plot_subresults(subplot[0], actual_fres, actual_tres)

    subplot[1].set_xlabel("Expected TRE", fontsize=26)
    _plot_subresults(subplot[1], expected_tres, actual_tres)

    subplot[2].set_xlabel("Expected FRE", fontsize=26)
    _plot_subresults(subplot[2], expected_fres, actual_tres)

    subplot[3].set_xlabel("Expected FLE", fontsize=26)
    _plot_subresults(subplot[3], mean_fles, actual_tres)

    subplot[4].set_xlabel("Number of Fids.", fontsize=26)
    _plot_subresults(subplot[4], no_fids, actual_tres)

    plt.show()
