import os
import sys
import json
# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect, send_file
import numpy as np
from sksurgeryfredbe.algorithms.fit_contour import find_outer_contour
from sksurgeryfredbe.algorithms.point_based_reg import PointBasedRegistration
from sksurgeryfredbe.algorithms.fred import make_target_point, _is_valid_fiducial
from sksurgeryfredbe.algorithms.errors import expected_absolute_value
from sksurgeryfredbe.algorithms.fle import FLE
from sksurgeryfredbe import __version__ as fredversion
from util import base64_to_pil, contour_to_image, np_to_base64
from google.cloud import firestore

# Declare a flask app
app = Flask(__name__)

# Load model

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/contour', methods=['GET', 'POST'])
def contour():
    print("called contour")
    if request.method == 'POST':
        s1 = json.dumps(request.json)
        data =json.loads(s1)
        pil_image = base64_to_pil(data) # Returns pillow image
        np_image = np.array(pil_image)[:,:,:3]
        print(f'Left: {np_image.shape}')

        contour, init = find_outer_contour(np_image)
        contour = contour.astype(int) # cast to int
        contour = contour[1::5] #subsample every 5th element
        returnjson = jsonify({'contour': contour.tolist()})
        return returnjson


@app.route('/defaultcontour', methods=['GET', 'POST'])
def defaultcontour():
    print("called default contour")
    if request.method == 'POST':
        contour = np.load('static/brain512.npy')
        returnjson = jsonify({'contour': contour.tolist()})
        return returnjson


@app.route('/gettarget', methods=['GET', 'POST'])
def gettarget():
    if request.method == 'POST':
        s1 = json.dumps(request.json)
        outline =json.loads(s1)
        target = make_target_point(outline, edge_buffer=0.9)

        returnjson = jsonify({'target': target.tolist()})
        return returnjson


@app.route('/getfle', methods=['GET', 'POST'])
def getfle():
    if request.method == 'POST':
        fle_sd = np.random.uniform(low=0.5, high=5.0)
        moving_fle = np.array([0., 0., 0.], dtype=np.float64)
        fixed_fle = np.array([fle_sd, fle_sd, fle_sd], dtype=np.float64)
        fixed_fle_eavs = expected_absolute_value(fixed_fle)
        moving_fle_eavs = expected_absolute_value(moving_fle)

        returnjson = jsonify({
                'fixed_fle_sd': fixed_fle.tolist(),
                'moving_fle_sd': moving_fle.tolist(),
                'fixed_fle_eav': fixed_fle_eavs.tolist(),
                'moving_fle_eav': moving_fle_eavs.tolist()
                })
        return returnjson


@app.route('/placefiducial', methods=['GET', 'POST'])
def placefiducial():
    if request.method == 'POST':
        s1 = json.dumps(request.json)
        position = [json.loads(s1)[0], json.loads(s1)[1], 0.0]
        if _is_valid_fiducial(position):
            moving_fle = json.loads(s1)[2]
            fixed_fle = json.loads(s1)[3]

            fixed_fle = FLE(independent_fle = fixed_fle)
            moving_fle = FLE(independent_fle = moving_fle)

            fixed_fid = fixed_fle.perturb_fiducial(position);
            moving_fid = moving_fle.perturb_fiducial(position);

            returnjson = jsonify({
                'valid_fid': True,
                'fixed_fid': fixed_fid.tolist(),
                'moving_fid': moving_fid.tolist(),
                })
            return returnjson
        else:
            return jsonify({'valid_fid': False})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        s1 = json.dumps(request.json)
        position = [json.loads(s1)[0], json.loads(s1)[1], 0.0]
        target = np.array(json.loads(s1)[0])
        target = target.reshape(1,3)
        moving_fle_eav = json.loads(s1)[1]
        fixed_fle_eav = json.loads(s1)[2]
        moving_fids = np.array(json.loads(s1)[3])
        fixed_fids = np.array(json.loads(s1)[4])
        print (target)
        registerer = PointBasedRegistration(target, 
                        fixed_fle_eav, moving_fle_eav)

        [success, fre, fixed_fle_esv, expected_tre_squared,
                expected_fre_sq, transformed_target, actual_tre,
                no_fids] = registerer.register(fixed_fids, moving_fids)
        
        returnjson = jsonify({
                'success': success,
                'fre': fre,
                'fixed_fle_esv': fixed_fle_esv,
                'expected_tre_squared': expected_tre_squared,
                'expected_fre_sq': expected_fre_sq,
                'transformed_target': transformed_target.tolist(),
                'actual_tre': actual_tre,
                'no_fids': no_fids
                })

        return returnjson

@app.route('/initdatabase', methods=['GET', 'POST'])
def initdatabase():
        """
        here we will create a new document in collection results and 
        return the name of the document. Write some stuff about the date 
        and the versions of fred, core, and fredweb. Create a sub 
        collection of results within the document
        """
        db = firestore.Client()
        #create a new document in the results collection
        docRef = db.collection("results").add({
             'fred verion': fredversion,
             'fred web verion': '0.0.0'
        })
        print (docRef[1].id)
        return jsonify({'success': True,
                        'reference': docRef[1].id});

@app.route('/writeresults', methods=['GET', 'POST'])
def writeresults():
    if request.method == 'POST':
        s1 = json.dumps(request.json)
        print(s1)
        reference=json.loads(s1)[0]
        fre=json.loads(s1)[1]
        tre=json.loads(s1)[2]
        print ("writing results",fre, tre)
        db = firestore.Client()
        db.collection("results").document(reference).collection("results").add({
             'fre': fre,
             'tre': tre
        })
        return jsonify({'write OK': True})




if __name__ == '__main__':
     app.run(port=5002, threaded=True)

