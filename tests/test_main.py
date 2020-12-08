# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
import pytest
import main as sksfmain # pylint: disable=unused-import

# Pytest style

# pylint: disable=redefined-outer-name
@pytest.fixture
def client():
    """
    A fixture to use Flask's testing skeleton
    https://flask.palletsprojects.com/en/1.1.x/testing/
    """
    with sksfmain.app.test_client() as myclient:
        yield myclient


def testserveindex(client):
    """Serve up the index page"""

    _index = client.get('/')
    #print (_index.data)
