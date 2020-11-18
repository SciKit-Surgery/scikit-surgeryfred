import os
import sys
import json
# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect, send_file
import numpy as np
from sksurgeryfred.algorithms.fit_contour import find_outer_contour
from sksurgeryfred.algorithms.fred import make_target_point
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
        #with open('brain512.npy', 'wb') as fileout:
        #    np.save(fileout, contour)
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


if __name__ == '__main__':
     app.run(port=5002, threaded=True)

