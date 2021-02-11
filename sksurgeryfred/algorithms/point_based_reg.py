"""Functions to support MedPhys Taught Module workshop on
calibration and tracking
"""

import numpy as np

from sksurgerycore.algorithms.procrustes import orthogonal_procrustes
from sksurgerycore.algorithms.errors import compute_tre_from_fle, \
                compute_fre_from_fle


class PointBasedRegistration:
    """
    Does the registration and assoctiated measures
    """

    def __init__(self, target, fixed_fle_esv, moving_fle_esv):
        """
        :params target: 1x3 target point
        :params fixed_fle_esv: the expected squared value of the fixed image fle
        :params moving_fle_esv: the expected squared value of the moving
            image fle
        """
        if not moving_fle_esv == 0.0:
            raise NotImplementedError("Currently we only support zero" +
                                      "fle on moving image ")

        self.target = None
        self.fixed_fle_esv = None
        self.moving_fle_esv = None
        self.transformed_target = None
        self.reinit(target, fixed_fle_esv, moving_fle_esv)

    def reinit(self, target, fixed_fle_esv, moving_fle_esv):
        """
        reinitiatilses the target and errors
        """
        self.target = target
        self.fixed_fle_esv = fixed_fle_esv
        self.moving_fle_esv = moving_fle_esv
        self.transformed_target = None

    def register(self, fixed_points, moving_points):
        """
        Does the registration
        """
        success = False
        fre = 0.0
        expected_tre_squared = 0.0
        expected_fre_sq = 0.0
        actual_tre = 0.0
        self.transformed_target = np.zeros(shape=(1, 3), dtype=np.float64)
        no_fids = fixed_points.shape[0]

        if no_fids > 2:
            rotation, translation, fre = orthogonal_procrustes(
                fixed_points, moving_points)
            expected_tre_squared = compute_tre_from_fle(
                moving_points[:, 0:3], self.fixed_fle_esv, self.target[:, 0:3])
            expected_fre_sq = compute_fre_from_fle(moving_points[:, 0:3],
                                                   self.fixed_fle_esv)

            self.transformed_target = np.matmul(rotation,
                                                self.target.transpose()) + \
                                               translation
            actual_tre = np.linalg.norm(
                self.transformed_target - self.target[:, 0:3].transpose())
            success = True


        return [success, fre, self.fixed_fle_esv, expected_tre_squared,
                expected_fre_sq, self.transformed_target[:, 0:3], actual_tre,
                no_fids]

    def get_transformed_target(self):
        """
        Returns transformed target and status
        """
        if self.transformed_target is not None:
            return True, self.transformed_target[:, 0:3]

        return False, None
