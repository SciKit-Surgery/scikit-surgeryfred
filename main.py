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
from util import base64_to_pil, contour_to_image, np_to_base64
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


if __name__ == '__main__':
     app.run(port=5002, threaded=True)

