# coding=utf-8

"""Command line processing"""


import argparse
from sksurgeryfred import __version__
from sksurgeryfred.ui.sksurgeryfred_game import run_demo


def main(args=None):
    """
    Entry point for Fiducial Registration Educational Demonstration
    application"""

    parser = argparse.ArgumentParser(
        description='Fiducial Registration Educational Demonstration - Game')

    ## ADD POSITIONAL ARGUMENTS
    parser.add_argument("image",
                        type=str,
                        help="Image file name")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='Fiducial Registration Educational Demonstration version ' + \
                        friendly_version_string)

    args = parser.parse_args(args)

    run_demo(args.image)
