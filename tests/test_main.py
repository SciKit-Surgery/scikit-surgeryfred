# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
from html.parser import HTMLParser
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

class FredHTMLParser(HTMLParser): #pylint: disable = abstract-method
    """Parse the html back from index.html"""
    def __init__(self, title):
        super().__init__()
        self.found_title = False
        self.title_ok = False
        self.target_title = title

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.found_title = not self.found_title
        else:
            self.found_title = False

    def handle_data(self, data):
        if self.found_title:
            if data == self.target_title:
                self.title_ok = True
            self.found_title = False


def testserveindex(client):
    """Serve up the index page"""

    index = client.get('/')
    parser = FredHTMLParser('SciKit-SurgeryFRED')
    parser.feed(str(index.data))
    assert parser.title_ok

    index = client.post('/')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(index.data))
    assert parser.title_ok
