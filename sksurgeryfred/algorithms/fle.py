#  -*- coding: utf-8 -*-

"""
Functions for adding fiducial localisation error
"""

import numpy as np


def _set_fle(fle, dims):
    """ Internal function to check and set the fle """
    if isinstance(fle, np.ndarray):
        if fle.size == 1:
            fle_array = np.full(dims, fle.item(0), dtype=np.float64)
        else:
            if fle.size != dims:
                raise ValueError("FLE value must be single value or array",
                                 " of length ", dims)
            return fle
    else:
        fle_array = np.full(dims, fle, dtype=np.float64)

    assert fle_array.size == dims
    return fle_array

class FLE:
    """
    Provides methods to add Fiducial Localisation Error to a point

    :param independent_fle: the magnitude(s) of the independent FLE's,
        used for the default ind_fle_function. Do not use if using
        your own ind_fle_function. A single float
        will yield isotropic error, or an array can be passed for
        anisotropic errors.
    :param ind_fle_function: the function to use for sampling the independent
        fle. Defaults to numpy.random.normal
    :param systematic_fle: the magnitude(s) of the systematic FLE's,
        used for the default sys_fle_function. Do not use if using
        your own sys_fle_function. A single float
        will yield isotropic error, or an array can be passed for
        anisotropic errors.
    :param sys_fle_function: the function to use for sampling the independent
        fle. Defaults to numpy.add
    :param dimension: the dimensions to use, defaults to 3.

    :raises ValueError: If independent_fle is not single value or array of
        length dimension.
    :raises ValueError: If both fle function and fle value are set.
    :raises TypeError: If either error function is invalid.

    """

    def __init__(self, independent_fle=None, ind_fle_function=None,
                 systematic_fle=None, sys_fle_function=None, dimension=3):

        if ind_fle_function is None:
            if independent_fle is None:
                independent_fle = 0.0
            ind_fle = _set_fle(independent_fle, dimension)
            def ind_fle_function():
                return np.random.normal(loc=0.0, scale=ind_fle, size=dimension)
        else:
            if independent_fle is not None:
                raise ValueError("Set independent_fle and ind_fle_function, ",
                                 "independent_fle will be ignored")
        self.ind_fle_function = ind_fle_function

        try:
            self.ind_fle_function()
        except TypeError:
            raise TypeError("Failed to run function, ", ind_fle_function,
                            "check function") from TypeError

        if sys_fle_function is None:
            if systematic_fle is None:
                systematic_fle = 0.0
            sys_fle = _set_fle(systematic_fle, dimension)
            def sys_fle_function():
                return sys_fle
        else:
            if systematic_fle is not None:
                raise ValueError("Set systematic_fle and sys_fle_function, ",
                                 "systematic_fle will be ignored")
        self.sys_fle_function = sys_fle_function

        try:
            self.sys_fle_function()
        except TypeError:
            raise TypeError("Failed to run function, ", sys_fle_function,
                            "check function") from TypeError

    def perturb_fiducial(self, fiducial_marker):
        """
        Adds the FLE to the marker position

        :param fiducial_marker: the true position of the marker.
        :returns: The perturbed position of the marker
        """
        return fiducial_marker + self.sys_fle_function() + \
                        self.ind_fle_function()
