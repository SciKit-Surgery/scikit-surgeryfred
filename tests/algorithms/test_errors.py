# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import numpy as np

import sksurgeryfred.algorithms.errors as e2d

# Pytest style

def _eav_by_brute_force(stddevs):

    cum_sum = 0.0
    for _ in range(1000):
        error = np.random.normal(
            loc=np.zeros(np.array(stddevs).shape),
            scale=stddevs)
        fle = np.linalg.norm(error)
        cum_sum += (fle * fle)

    eavs = cum_sum/1000.0

    return eavs

def test_expected_absolute_value_1d():
    """
    Tests that expected absolute value works for the one dimensional case
    """
    np.random.seed(0)
    stddevs = np.array([0.0], dtype=np.float64)

    stddevs[0] = 0.0
    eav = e2d.expected_absolute_value(stddevs)

    assert eav == 0.0
    assert eav == _eav_by_brute_force(stddevs)

    stddevs[0] = 1.0
    eav = e2d.expected_absolute_value(stddevs)

    arith_eav = np.linalg.norm(stddevs)
    arith_eav *= arith_eav
    assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
    #absolute(a - b) <= (atol + rtol * absolute(b))
    #so rtol = 0.1 is around 10% rtol = 0.01 is 1 %
    assert np.isclose(eav, _eav_by_brute_force(stddevs), atol=0.0, rtol=0.15)

    for _ in range(10):
        stddevs[0] = np.absolute(np.random.normal()*10.0)
        eav = e2d.expected_absolute_value(stddevs)

        arith_eav = np.linalg.norm(stddevs)
        arith_eav *= arith_eav
        assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
        assert np.isclose(eav, _eav_by_brute_force(stddevs),
                          atol=0.0, rtol=0.15)


def test_expected_absolute_value_2d():
    """
    Tests that expected absolute value works for the two dimensional case
    """
    np.random.seed(0)
    stddevs = np.array([0.0, 0.0], dtype=np.float64)

    stddevs = [0.0, 0.0]
    eav = e2d.expected_absolute_value(stddevs)

    assert eav == 0.0
    assert eav == _eav_by_brute_force(stddevs)

    stddevs = np.array([1.0, 1.0], dtype=np.float64)
    eav = e2d.expected_absolute_value(stddevs)

    arith_eav = np.linalg.norm(stddevs)
    arith_eav *= arith_eav
    assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
    assert np.isclose(eav, _eav_by_brute_force(stddevs), atol=0.0, rtol=0.05)

    for _ in range(10):
        stddevs = np.absolute(np.random.normal((1, 1))*10.0)
        eav = e2d.expected_absolute_value(stddevs)
        arith_eav = np.linalg.norm(stddevs)
        arith_eav *= arith_eav
        assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
        assert np.isclose(eav, _eav_by_brute_force(stddevs),
                          atol=0.0, rtol=0.15)



def test_expected_absolute_value_3d():
    """
    Tests that expected absolute value works for the three dimensional case
    """
    np.random.seed(0)
    stddevs = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    eav = e2d.expected_absolute_value(stddevs)

    assert eav == 0.0
    assert eav == _eav_by_brute_force(stddevs)

    stddevs = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    eav = e2d.expected_absolute_value(stddevs)

    arith_eav = np.linalg.norm(stddevs)
    arith_eav *= arith_eav
    assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
    assert np.isclose(eav, _eav_by_brute_force(stddevs), atol=0.0, rtol=0.15)

    for _ in range(10):
        stddevs = np.absolute(np.random.normal((1, 1, 1))*10.0)
        eav = e2d.expected_absolute_value(stddevs)
        arith_eav = np.linalg.norm(stddevs)
        arith_eav *= arith_eav
        assert np.isclose(eav, arith_eav, atol=0.0, rtol=0.0001)
        assert np.isclose(eav, _eav_by_brute_force(stddevs),
                          atol=0.0, rtol=0.15)
