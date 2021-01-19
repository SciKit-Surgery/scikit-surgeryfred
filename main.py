"""
Module to handle communication between client (static/main.js) and
sksurgeryfred server
"""
import json
import math
import datetime
# Flask
from flask import Flask, request, render_template, jsonify

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
