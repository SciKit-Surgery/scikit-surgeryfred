# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""
from html.parser import HTMLParser
import json
import pytest
import numpy as np
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

def testserve_defaultcontour(client):
    """Serve default contour"""
    #get should not be allowed
    contour = client.get('/defaultcontour')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(contour.data))
    assert parser.title_ok

    #returns a default contour defined at static/brain512.npy
    response = client.post('/defaultcontour')
    expectedcontour = np.load('static/brain512.npy')
    servedcontour = json.loads(response.data.decode()).get('contour')

    assert np.array_equal(servedcontour, expectedcontour)

def testserve_gettarget(client):
    """Serve target"""
    #get should not be allowed
    target = client.get('/gettarget')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(target.data))
    assert parser.title_ok

    #should return a 2D target point
    contour = np.load('static/brain512.npy')
    postdata = dict(outline=contour.tolist())
    response = client.post('/gettarget',
                    data = json.dumps(postdata),
                    content_type='application/json')
    target = json.loads(response.data.decode()).get('target')

    assert len(target[0]) == 3
    assert target[0][2] == 0.0

def testserve_getfle(client):
    """Serve fle"""
    #get should not be allowed
    fle = client.get('/getfle')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(fle.data))
    assert parser.title_ok

    #test the default values
    returndata = client.post('/getfle')
    fles = json.loads(returndata.data.decode())
    fixed_fle_sd = np.array(fles.get('fixed_fle_sd'))
    moving_fle_sd = np.array(fles.get('moving_fle_sd'))
    fixed_fle_eav = np.array(fles.get('fixed_fle_eav'))
    moving_fle_eav = np.array(fles.get('moving_fle_eav'))

    exp_fixed_eav = np.linalg.norm(fixed_fle_sd)**2
    assert np.all(fixed_fle_sd == fixed_fle_sd[0])
    assert np.all(fixed_fle_sd >= 0.5)
    assert np.all(fixed_fle_sd <= 5.0)
    assert np.all(moving_fle_sd == 0.0)
    assert fixed_fle_eav == exp_fixed_eav
    assert moving_fle_eav == 0.0

def testserve_placefiducial(client):
    """Serve place fiducial"""
    #get should not be allowed
    fid = client.get('/placefiducial')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(fid.data))
    assert parser.title_ok

    #normal usage
    x_pos = 0.0
    y_pos = 0.0
    pre_op_ind_fle = [0.0, 0.0, 0.0]
    intra_op_ind_fle = [2.0, 2.0, 2.0]
    postdata = dict(
             x_pos=x_pos,
             y_pos=y_pos,
             pre_op_ind_fle=pre_op_ind_fle,
             intra_op_ind_fle=intra_op_ind_fle)
    fid = client.post('/placefiducial', data = json.dumps(postdata),
                    content_type='application/json')
    assert json.loads(fid.data.decode()).get("valid_fid")

    #we should be able to apply a systematic error
    x_pos = 100.0
    y_pos = 250.0
    pre_op_sys_fle = [0.0, 0.0, 0.0]
    intra_op_sys_fle = [2.0, 2.0, -2.0]
    postdata = dict(
             x_pos=x_pos,
             y_pos=y_pos,
             pre_op_sys_fle=pre_op_sys_fle,
             intra_op_sys_fle=intra_op_sys_fle)
    fid = client.post('/placefiducial', data = json.dumps(postdata),
                    content_type='application/json')

    intra_op_fid = json.loads(fid.data.decode()).get("fixed_fid")
    pre_op_fid = json.loads(fid.data.decode()).get("moving_fid")
    assert intra_op_fid == [102.0, 252.0, -2.0]
    assert pre_op_fid == [100.0, 250.0, 0.0]


def testserve_register(client):
    """Serve register"""
    #get should not be allowed
    reg = client.get('/register')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(reg.data))
    assert parser.title_ok

def testserve_initdatabase(client):
    """Serve init db"""
    #get should not be allowed
    database = client.get('/initdatabase')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(database.data))
    assert parser.title_ok

def testserve_writeresults(client):
    """Serve write results"""
    #get should not be allowed
    database = client.get('/writeresults')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(database.data))
    assert parser.title_ok

def testserve_correlation(client):
    """Serve default contour"""
    #get should not be allowed
    corr = client.get('/correlation')
    parser = FredHTMLParser('405 Method Not Allowed')
    parser.feed(str(corr.data))
    assert parser.title_ok
