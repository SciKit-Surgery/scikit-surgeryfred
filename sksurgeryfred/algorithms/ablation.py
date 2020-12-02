#  -*- coding: utf-8 -*-

"""
Functions for point based registration using Orthogonal Procrustes.
"""

from sksurgeryfredbe.algorithms.scores import calculate_score

class Ablator():
    """
    handles the simulated ablation for scikit-surgery fred
    """
    def __init__(self, margin):
        """
        Initialise ablator with some empty member variables
        """
        self.margin = margin
        self.target = None
        self.est_target = None
        self.target_radius = None
        self.ready = False
        self.margin_increment = 0.1

    def setup(self, target, target_radius):
        """
        Setup target etc.
        """
        self.target = target
        self.target_radius = target_radius
        self.ready = True

    def increase_margin(self):
        """
        Make the margin bigger
        """
        if self.ready:
            self.margin += self.margin_increment
            return self.margin
        return 0.0

    def decrease_margin(self):
        """
        Make the margin smaller
        """
        if self.ready:
            self.margin -= self.margin_increment
            if self.margin <= 0.0:
                self.margin = 0.0
            return self.margin
        return 0.0


    def ablate(self, estimated_target):
        """
        performs and ablation, returns a score.
        """
        if not self.ready:
            return None
        score = calculate_score(self.target, estimated_target.transpose(),
                                self.target_radius, self.margin)
        return score
