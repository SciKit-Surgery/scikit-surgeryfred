"""
Module to handle communication between client (static/main.js) and
sksurgeryfred server
"""
import json
import math
import datetime
# Flask
from flask import Flask, request, render_template, jsonify
import numpy as np
from google.cloud import firestore
from google.auth.exceptions import DefaultCredentialsError
from sksurgeryfred.algorithms.point_based_reg import PointBasedRegistration
from sksurgeryfred.algorithms.fred import make_target_point, is_valid_fiducial
from sksurgeryfred.algorithms.errors import expected_absolute_value
from sksurgeryfred.algorithms.fle import FLE
from sksurgeryfred.algorithms.scores import calculate_score
from sksurgeryfred.utilities.results_database import ResultsDatabase
from sksurgeryfred import __version__ as fredversion

# Declare a flask app
app = Flask(__name__)

# Load model

@app.route('/', methods=['GET'])
def index():
    """
    returns the main page, template/index.html
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5002, threaded=True)
