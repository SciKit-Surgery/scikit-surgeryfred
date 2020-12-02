# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import numpy as np
from scipy import stats
import pytest

from sksurgeryfred.algorithms.fle import FLE

def test_fle_default():
    """Tests for FLE default"""

    #test default works
    fixed_fle = FLE()

    fiducial_location = np.array([1.0, 2.0, 0.0])
    moved_location = fixed_fle.perturb_fiducial(fiducial_location)
    assert np.array_equal(fiducial_location, moved_location)

def test_fle_with_values():
    """
    Tests that FLE works when we pass in values
    """
    np.random.seed(0)
    #test we can init with single value FLE
    independent_fle = 1.0
    ind_fle_function = None
    systematic_fle = 0.0
    sys_fle_function = None
    dimension = 3
    fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                    sys_fle_function, dimension)

    fiducial_location = np.array([1.0, 2.0, 0.0])
    repeats = 1000
    samples = np.zeros((repeats, dimension), dtype=np.float64)
    for index in range(repeats):
        samples[index] = fixed_fle.perturb_fiducial(fiducial_location)

    test_threshold = 0.10
    #all samples should not be normal, as they have different means
    _k2_all, p_all = stats.normaltest(samples, axis=None)
    assert p_all < test_threshold

    #subtract the means and retest
    _k2_all, p_all = stats.normaltest(samples - fiducial_location, axis=None)
    assert p_all > test_threshold

    #test we can init with an array
    systematic_fle = np.full(1, 2.0, dtype=np.float64)
    independent_fle = np.array([2.0, 1.0], dtype=np.float64)
    dimension = 2
    fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                    sys_fle_function, dimension)

    fiducial_location = np.array([1.0, 0.0])
    samples = np.zeros((repeats, dimension), dtype=np.float64)
    for index in range(repeats):
        samples[index] = fixed_fle.perturb_fiducial(fiducial_location)

    #all samples should not be normal, as they have different standard devs
    _k2_all, p_all = stats.normaltest(samples, axis=None)
    assert p_all < test_threshold

    #normalise for means
    _k2_all, p_all = stats.normaltest(samples - fiducial_location
                                      - np.full(2, 2.0, dtype=np.float64),
                                      axis=None)
    assert p_all < test_threshold

    #normalise for means and stddevs
    _k2_all, p_all = stats.normaltest((samples - fiducial_location
                                       - np.full(2, 2.0, dtype=np.float64))/
                                      independent_fle,
                                      axis=None)
    assert p_all > test_threshold


def test_fle_with_wrong_params():
    """
    Tests that init raises exceptions in error conditions
    """
    #test we get a value error if the array is the wrong size
    independent_fle = 1.0
    ind_fle_function = None
    systematic_fle = 0.0
    sys_fle_function = None
    dimension = 2
    systematic_fle = np.full(3, 2.0, dtype=np.float64)

    with pytest.raises(ValueError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)

    #test we get value error when we set both function and value
    systematic_fle = 1.0
    def my_add():
        return np.full(2, 2.0, dtype=np.float64)
    sys_fle_function = my_add
    with pytest.raises(ValueError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)
    ind_fle_function = my_add
    with pytest.raises(ValueError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)

    #test we get type errors if the function is wrong
    def my_bad_add(array_a):
        return array_a

    sys_fle_function = my_bad_add
    systematic_fle = None
    ind_fle_function = None
    with pytest.raises(TypeError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)
    ind_fle_function = my_bad_add
    independent_fle = None
    with pytest.raises(TypeError):
        _fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                         sys_fle_function, dimension)


def test_fle_with_custom_function():
    """Test that custom function works"""
    independent_fle = None
    ind_fle_function = None
    systematic_fle = None
    sys_fle_function = None
    dimension = 2

    #test we can pass our own function
    def my_add():
        return np.full(2, 2.0, dtype=np.float64)

    ind_fle_function = my_add
    fixed_fle = FLE(independent_fle, ind_fle_function, systematic_fle,
                    sys_fle_function, dimension)

    fiducial_location = np.array([1.0, 0.0])
    assert np.array_equal(fixed_fle.perturb_fiducial(fiducial_location),
                          np.array([3.0, 2.0]))
