#  -*- coding: utf-8 -*-

"""
Functions for point based registration using Orthogonal Procrustes.
"""

import numpy as np


def expected_absolute_value(std_devs):
    """
    Returns the expected absolute value of a normal
    distribution with mean 0 and standard deviations std_dev
    """

    onedsd = np.linalg.norm(std_devs)
    variance = onedsd * onedsd
    return variance
