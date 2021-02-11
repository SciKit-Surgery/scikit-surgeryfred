# coding=utf-8

"""Command line processing"""


import argparse
from sksurgeryfred import __version__
from sksurgeryfred.ui.sksurgeryfred_plotter import run_plotter


def main(args=None):
    """
    Entry point for Fiducial Registration Educational Demonstration
    application"""

    parser = argparse.ArgumentParser(
        description=('Plot Results for Fiducial Registration' +
                     'Educational Demonstration'))

    ## ADD POSITIONAL ARGUMENTS
    parser.add_argument("logfile",
                        type=str,
                        help="Log file name")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='Fiducial Registration Educational Demonstration version ' + \
                        friendly_version_string)

    args = parser.parse_args(args)

    run_plotter(args.logfile)
