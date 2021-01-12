"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import math
import numpy as np

def is_valid_fiducial(fiducial_location):
    """
    Checks the x, y, and z location of a fiducial
    :returns: true if a valid fiducial
    """
    #no negatives allowed
    if np.all(np.array(fiducial_location) >= 0):
        return True
    return False

def make_target_point(outline, edge_buffer=0.9):
    """
    returns a target point, that should lie
    within the outline.
    """
    #let's assume the anatomy is a circle with
    #centre, and radius
    centre = np.mean(outline, 0)
    max_radius = np.min((np.max(outline, 0) - np.min(outline, 0))/2)*edge_buffer
    radius = np.random.uniform(low=0.0, high=max_radius)
    radius = np.random.uniform(low=0.0, high=max_radius)
    angle = np.random.uniform(low=0.0, high=math.pi*2.0)
    x_ord = radius * math.cos(angle) + centre[0]
    y_ord = radius * math.sin(angle) + centre[1]
    return np.array([[x_ord, y_ord, 0.0]])
