# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import math
import numpy as np

import sksurgeryfred.algorithms.scores as scores

# Pytest style

def test_spheres_no_overlap():
    """
    Should return zero if no overlap
    """
    centre0 = np.array([-10.0, -10.0, -10.0])
    centre1 = np.array([10.0, 10.0, 10.0])
    radius0 = 10.0
    radius1 = 10.0

    overlap = scores.two_sphere_overlap_volume(centre0, centre1,
                                               radius0, radius1)

    assert np.isclose(overlap, 0.0, atol=0.0, rtol=0.0)

def test_spheres_same_centres():
    """
    Should return volume of smallest sphere if coincident
    """
    centre0 = np.array([-5.0, -6.5, 4])
    centre1 = np.array([-5.0, -6.5, 4])
    radius0 = 8.0
    radius1 = 10.0

    overlap = scores.two_sphere_overlap_volume(centre0, centre1,
                                               radius0, radius1)

    volume = math.pi * 4.0 / 3.0 * 8.0 * 8.0 * 8.0
    assert np.isclose(overlap, volume, atol=0.0, rtol=0.0)

    overlap = scores.two_sphere_overlap_volume( #pylint: disable=arguments-out-of-order
        centre1, centre0, radius1, radius0)

    assert np.isclose(overlap, volume, atol=0.0, rtol=0.0)

def test_spheres_full_overlap():
    """
    Should return the volume of the smallest sphere if totally covered
    """
    centre0 = np.array([-5.0, -6.5, 4.0])
    centre1 = np.array([-1.0, -3.5, 2.0])
    radius0 = 8.0
    radius1 = 2.0

    volume = math.pi * 4.0 / 3.0 * 2.0 * 2.0 * 2.0
    overlap = scores.two_sphere_overlap_volume(centre0, centre1,
                                               radius0, radius1)

    assert np.isclose(overlap, volume, atol=0.0, rtol=0.0)
    overlap = scores.two_sphere_overlap_volume( #pylint: disable=arguments-out-of-order
        centre1, centre0, radius1, radius0)

    assert np.isclose(overlap, volume, atol=0.0, rtol=0.0)


def test_spheres_partial_overlap():
    """
    Should return the volume of the smallest sphere if totally covered
    """
    centre0 = np.array([-5.0, -6.5, 4.0])
    centre1 = np.array([-1.0, -3.5, 2.0])
    radius0 = 4.0
    radius1 = 2.0

    overlap = scores.two_sphere_overlap_volume(centre0, centre1,
                                               radius0, radius1)

    distance = math.sqrt(16.0 + 9.0 + 4)
    volume = (math.pi / (12.0 * distance) *
              (6 - distance)*(6 - distance) *
              (distance * distance + 2*distance*6.0 - 3.0 * 4.0))

    assert np.isclose(overlap, volume, atol=0.0, rtol=0.0)


def test_calc_score_perfect():
    """Hit all of the target and nothing else"""
    target_centre = np.array([100.0, 20.0, 0.0])
    est_target_centre = np.array([100.0, 20.0, 0.0])

    target_radius = 10.0
    margin = 0.0

    score = scores.calculate_score(
        target_centre, est_target_centre, target_radius, margin)

    assert score == 1000.0

def test_calc_score_miss():
    """Miss target and nothing else"""
    target_centre = np.array([100.0, 20.0, 0.0])
    est_target_centre = np.array([-100.0, 20.0, 0.0])

    target_radius = 10.0
    margin = 0.0

    score = scores.calculate_score(
        target_centre, est_target_centre, target_radius, margin)

    assert score == -1000.0

def test_calc_hit_with_damage():
    """Hit all of the target and nothing else"""
    target_centre = np.array([100.0, 20.0, 0.0])
    est_target_centre = np.array([110.0, 20.0, 0.0])

    target_radius = 10.0
    margin = 10.0

    score = scores.calculate_score(
        target_centre, est_target_centre, target_radius, margin)

    target_vol = math.pi * 4.0 / 3.0 * 1000.0
    treatment_vol = math.pi * 4.0 / 3.0 * 20.0 * 20.0 * 20.0
    myscore = 1000.0 - (1000.0 * (treatment_vol - target_vol)/treatment_vol)
    assert score == myscore
