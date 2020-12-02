#  -*- coding: utf-8 -*-

"""
Functions for calculating the score for ablation game
"""

import math
import numpy as np


def sphere_volume(radius):
    """
    :returns: the volume of a sphere of radius
    """
    return 4.0 * math.pi * radius * radius * radius / 3.0

def two_sphere_overlap_volume(centre0, centre1, radius0, radius1):
    """
    Calculates the overlapping volume of two spheres
    from https://math.stackexchange.com/questions/297751/overlapping-spheres
    :param: centre0 centre of sphere0 (1x3)
    :param: centre1 centre of sphere1 (1x3)
    :param: radius0 radius of sphere0 (1)
    :param: radius1 radius of sphere1 (1)
    """


    distance = np.linalg.norm(centre1 - centre0)

    sum_radii = radius0 + radius1
    abs_diff_radii = abs(radius0 - radius1)

    if distance >= sum_radii:
        return 0.0

    if distance <= abs_diff_radii:
        if radius0 < radius1:
            return sphere_volume(radius0)
        return sphere_volume(radius1)

    first_term = math.pi / (12 * distance)
    second_term = (sum_radii - distance) * (sum_radii - distance)
    third_term = (distance * distance +
                  2 * distance * sum_radii -
                  3 * abs_diff_radii * abs_diff_radii)

    return first_term * second_term * third_term


def calculate_score(target_centre, est_target_centre, target_radius, margin):
    """
    Calculates the score for a given simulated ablation
    :params target_centre: The known target position
    :params est_target_centre: The target centre estimated by registration
    :target_radius: The radius of the target
    :margin: The margin to add (treatment radius = target_radius + margin
    :returns: the score
    """
    target_volume = sphere_volume(target_radius)
    treatment_volume = sphere_volume(target_radius + margin)
    overlap_volume = two_sphere_overlap_volume(
        target_centre, est_target_centre,
        target_radius, target_radius + margin)

    target_not_treated = (target_volume - overlap_volume) / target_volume
    treatment_score = 1000.0
    if target_not_treated > 0.0:
        treatment_score = 0.0

    healty_tissue_treated = \
                    (treatment_volume - overlap_volume) / treatment_volume

    margin_penalty = -1000.0 * healty_tissue_treated

    return round(treatment_score + margin_penalty)
