# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import math
import numpy as np

from sksurgeryfred.algorithms.errors import expected_absolute_value
import sksurgeryfred.algorithms.point_based_reg as pbreg

def _make_circle_fiducials(no_fids, centre, radius,
                           fixed_stddevs, moving_stddevs):

    fixed_fids = np.zeros(shape=(no_fids, 3), dtype=np.float64)
    moving_fids = np.zeros(shape=(no_fids, 3), dtype=np.float64)

    angle_inc = math.pi * 2.0 / float(no_fids)

    for fid in range(no_fids):
        fixed_fids[fid] = ([radius * math.cos(angle_inc*fid),
                            radius * math.sin(angle_inc*fid),
                            0.0] +
                           np.random.normal(scale=fixed_stddevs) +
                           centre)

        moving_fids[fid] = ([radius * math.cos(angle_inc*fid),
                             radius * math.sin(angle_inc*fid),
                             0.0] +
                            np.random.normal(scale=moving_stddevs) +
                            centre)

    return fixed_fids, moving_fids


def test_pbr_3_fids():
    """
    Tests for tre_from_fle_2d
    """
    fixed_fle_std_dev = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    moving_fle_std_dev = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    fixed_fle_easv = expected_absolute_value(fixed_fle_std_dev)
    moving_fle_easv = expected_absolute_value(moving_fle_std_dev)

    target = np.array([[0.0, 0.0, 0.0]], dtype=np.float64)

    pbr = pbreg.PointBasedRegistration(target, fixed_fle_easv, moving_fle_easv)

    centre = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    radius = 20.0

    tresq_sum = 0
    fresq_sum = 0
    expected_tre_squared = 0
    expected_fre = 0
    repeats = 100
    for _ in range(repeats):
        fixed_fids, moving_fids = _make_circle_fiducials(3, centre, radius,
                                                         fixed_fle_std_dev,
                                                         moving_fle_std_dev)


        [_success, fre, _mean_fle, expected_tre_squared, expected_fre,
         _transformed_target_2d, actual_tre, _no_fids] = pbr.register(
             fixed_fids, moving_fids)

        tresq_sum += actual_tre*actual_tre
        fresq_sum += fre*fre

    ave_tresq = tresq_sum/repeats
    ave_fresq = fresq_sum/repeats

    assert np.isclose(ave_tresq, expected_tre_squared, atol=0.0, rtol=0.10)
    assert np.isclose(ave_fresq, expected_fre, atol=0.0, rtol=0.05)

def test_pbr_10_fids():
    """
    Tests for tre_from_fle_2d
    """

    fixed_fle_std_dev = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    moving_fle_std_dev = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    fixed_fle_easv = expected_absolute_value(fixed_fle_std_dev)
    moving_fle_easv = expected_absolute_value(moving_fle_std_dev)

    target = np.array([[0.0, 0.0, 0.0]], dtype=np.float64)

    pbr = pbreg.PointBasedRegistration(target, fixed_fle_easv, moving_fle_easv)

    centre = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    radius = 2.0

    tresq_sum = 0
    fresq_sum = 0
    expected_tre_squared = 0
    expected_fre = 0
    repeats = 100
    for _ in range(repeats):
        fixed_fids, moving_fids = _make_circle_fiducials(10, centre, radius,
                                                         fixed_fle_std_dev,
                                                         moving_fle_std_dev)


        [_success, fre, _mean_fle, expected_tre_squared, expected_fre,
         _transformed_target_2d, actual_tre, _no_fids] = pbr.register(
             fixed_fids, moving_fids)

        tresq_sum += actual_tre*actual_tre
        fresq_sum += fre*fre

    ave_tresq = tresq_sum/repeats
    ave_fresq = fresq_sum/repeats

    assert np.isclose(ave_tresq, expected_tre_squared, atol=0.0, rtol=0.10)
    assert np.isclose(ave_fresq, expected_fre, atol=0.0, rtol=0.05)

def test_pbr_10_fids_offset_target():
    """
    Tests for tre_from_fle_2d
    """

    fixed_fle_std_dev = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    moving_fle_std_dev = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    fixed_fle_easv = expected_absolute_value(fixed_fle_std_dev)
    moving_fle_easv = expected_absolute_value(moving_fle_std_dev)

    target = np.array([[2.0, 1.0, 0.0]], dtype=np.float64)

    pbr = pbreg.PointBasedRegistration(target, fixed_fle_easv, moving_fle_easv)

    centre = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    radius = 2.0

    tresq_sum = 0
    fresq_sum = 0
    expected_tre_squared = 0
    expected_fre = 0
    repeats = 400
    for _ in range(repeats):
        fixed_fids, moving_fids = _make_circle_fiducials(10, centre, radius,
                                                         fixed_fle_std_dev,
                                                         moving_fle_std_dev)


        [_success, fre, _mean_fle, expected_tre_squared, expected_fre,
         _transformed_target_2d, actual_tre, _no_fids] = pbr.register(
             fixed_fids, moving_fids)

        tresq_sum += actual_tre*actual_tre
        fresq_sum += fre*fre

    ave_tresq = tresq_sum/repeats
    ave_fresq = fresq_sum/repeats

    assert np.isclose(ave_tresq, expected_tre_squared, atol=0.0, rtol=0.10)
    assert np.isclose(ave_fresq, expected_fre, atol=0.0, rtol=0.05)

def test_pbr_20_fids_offset_target():
    """
    Tests for tre_from_fle_2d
    """

    fixed_fle_std_dev = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    moving_fle_std_dev = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    fixed_fle_easv = expected_absolute_value(fixed_fle_std_dev)
    moving_fle_easv = expected_absolute_value(moving_fle_std_dev)

    target = np.array([[2.0, 1.0, 0.0]], dtype=np.float64)

    pbr = pbreg.PointBasedRegistration(target, fixed_fle_easv, moving_fle_easv)

    centre = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    radius = 20.0

    tresq_sum = 0
    fresq_sum = 0
    expected_tre_squared = 0
    expected_fre = 0
    repeats = 400
    for _ in range(repeats):
        fixed_fids, moving_fids = _make_circle_fiducials(20, centre, radius,
                                                         fixed_fle_std_dev,
                                                         moving_fle_std_dev)


        [_success, fre, _mean_fle, expected_tre_squared, expected_fre,
         _transformed_target_2d, actual_tre, _no_fids] = pbr.register(
             fixed_fids, moving_fids)

        tresq_sum += actual_tre * actual_tre
        fresq_sum += fre * fre

    ave_tresq = tresq_sum/repeats
    ave_fresq = fresq_sum/repeats

    assert np.isclose(ave_tresq, expected_tre_squared, atol=0.0, rtol=0.10)
    assert np.isclose(ave_fresq, expected_fre, atol=0.0, rtol=0.05)
