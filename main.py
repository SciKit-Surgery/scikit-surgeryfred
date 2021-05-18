"""
Module to handle communication between client (static/main.js) and
sksurgeryfred server
"""
import json
import math
import datetime
# Flask
from flask import Flask, request, render_template, jsonify, send_file
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

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """
    returns the icon
    """
    return send_file('favicon.ico', mimetype='image/ico')


@app.route('/', methods=['GET'])
def index():
    """
    returns the main page, template/index.html
    """
    return render_template('index.html')

@app.route('/startfred', methods=['POST'])
def startfred():
    """
    returns the fred page
    """
    return render_template('fred.html')

@app.route('/defaultcontour', methods=['POST'])
def defaultcontour():
    """
    Returns a pre-calculated contour image to represent the
    intraoperative image.
    """
    contour = np.load('static/brain512.npy')
    returnjson = jsonify({'contour': contour.tolist()})
    return returnjson


@app.route('/gettarget', methods=['POST'])
def gettarget():
    """
    Returns a target point for the simulated intervention
    """
    jsonstring = json.dumps(request.json)
    outline =json.loads(jsonstring).get('outline')
    target = make_target_point(outline, edge_buffer=0.9)

    returnjson = jsonify({'target': target.tolist()})
    return returnjson


@app.route('/getfle', methods=['POST'])
def getfle():
    """
    Returns values for fiducial localisation errors
    Values are randomly selected from a uniform
    distribution from 0.5 to 5.0 pixels
    """
    fle_sd = np.random.uniform(low=0.5, high=5.0)
    #change fle_ratio if you want anisotropic fle
    fle_ratio = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    anis_scale = math.sqrt(3.0 / (np.linalg.norm(fle_ratio) ** 2))
    fixed_fle = fle_ratio * fle_sd * anis_scale

    moving_fle = np.array([0., 0., 0.], dtype=np.float64)
    fixed_fle_eavs = expected_absolute_value(fixed_fle)
    moving_fle_eavs = expected_absolute_value(moving_fle)

    returnjson = jsonify({
            'fixed_fle_sd': fixed_fle.tolist(),
            'moving_fle_sd': moving_fle.tolist(),
            'fixed_fle_eav': fixed_fle_eavs.tolist(),
            'moving_fle_eav': moving_fle_eavs.tolist()
            })
    return returnjson


@app.route('/placefiducial', methods=['POST'])
def placefiducial():
    """
    Returns the location of a fiducial marker on the pre-
    and intra-operative images. FLE is added to each
    marker location.
    """
    x_pos = request.json.get("x_pos")
    y_pos = request.json.get("y_pos")
    position = [x_pos, y_pos, 0.0]
    if is_valid_fiducial(position):
        moving_ind_fle = request.json.get("pre_op_ind_fle", [0., 0., 0.])
        fixed_ind_fle = request.json.get("intra_op_ind_fle", [0., 0., 0.])
        moving_sys_fle = request.json.get("pre_op_sys_fle", [0., 0., 0.])
        fixed_sys_fle = request.json.get("intra_op_sys_fle", [0., 0., 0.])

        fixed_fle = FLE(independent_fle = fixed_ind_fle,
                        systematic_fle = fixed_sys_fle)
        moving_fle = FLE(independent_fle = moving_ind_fle,
                         systematic_fle = moving_sys_fle)

        fixed_fid = fixed_fle.perturb_fiducial(position)
        moving_fid = moving_fle.perturb_fiducial(position)

        returnjson = jsonify({
            'valid_fid': True,
            'fixed_fid': fixed_fid.tolist(),
            'moving_fid': moving_fid.tolist(),
            })
        return returnjson

    return jsonify({'valid_fid': False})


@app.route('/register', methods=['POST'])
def register():
    """
    Performs point based registration and returns
    registration data as json.
    """
    jsonstring = json.dumps(request.json)
    reg_json = json.loads(jsonstring)
    target = np.array(reg_json.get("target"))
    target = target.reshape(1,3)
    moving_fle_eav = reg_json.get("preop_fle")
    fixed_fle_eav = reg_json.get("intraop_fle")
    moving_fids = np.array(reg_json.get("preop_fids"))
    fixed_fids = np.array(reg_json.get("intraop_fids"))
    registerer = PointBasedRegistration(target,
                    fixed_fle_eav, moving_fle_eav)

    [success, fre, mean_fle_sq, expected_tre_sq,
            expected_fre_sq, transformed_target, actual_tre,
            no_fids] = registerer.register(fixed_fids, moving_fids)

    expected_tre = 0.0
    expected_fre = 0.0
    mean_fle = 0.0

    if success:
        mean_fle = math.sqrt(mean_fle_sq)
        expected_tre = math.sqrt(expected_tre_sq)
        expected_fre = math.sqrt(expected_fre_sq)

    returnjson = jsonify({
            'success': success,
            'fre': fre,
            'mean_fle': mean_fle,
            'expected_tre': expected_tre,
            'expected_fre': expected_fre,
            'transformed_target': transformed_target.tolist(),
            'actual_tre': actual_tre,
            'no_fids': no_fids
            })

    return returnjson


@app.route('/initdatabase', methods=['POST'])
def initdatabase():
    """
    here we will create a new document in collection results and
    return the name of the document. Write some stuff about the date
    and the versions of fred, core, and fredweb. Create a sub
    collection of results within the document
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dbdict = {
             'fred verion': fredversion,
             'time': timestamp
             }
    try:
        database = firestore.Client()
        #create a new document in the results collection
        docref = database.collection("results").add(dbdict)
        return jsonify({'success': True,
                        'reference': docref[1].id})
    except DefaultCredentialsError:
        return jsonify({'success': False})

@app.route('/writeresults', methods=['POST'])
def writeresults():
    """
    write the results to a firestore database
    """
    jsonstring = json.dumps(request.json)
    result_json = json.loads(jsonstring)
    reference = result_json.get('reference')
    teststring = result_json.get('teststring', None)

    dbdict = {
             'actual_tre' : result_json.get('actual_tre'),
             'fre' : result_json.get('fre'),
             'expected_tre' : result_json.get('expected_tre'),
             'expected_fre' : result_json.get('expected_fre'),
             'mean_fle' : result_json.get('mean_fle'),
             'number_of_fids' : result_json.get('number_of_fids')
             }


    try:
        if teststring is not None:
            raise DefaultCredentialsError
        database = firestore.Client()
        reg_ref = database.collection("results").document(
                        reference).collection("results").add(dbdict)
        return jsonify({'write OK': True,
                        'reference': reg_ref[1].id})
    except DefaultCredentialsError:
        return jsonify({'write OK': False})


@app.route('/writegameresults', methods=['POST'])
def writegameresults():
    """
    write the game results to a firestore database
    """
    jsonstring = json.dumps(request.json)
    result_json = json.loads(jsonstring)
    reference = result_json.get('reference')
    teststring = result_json.get('teststring', None)

    dbdict = {
             'state': result_json.get('state'),
             'score': result_json.get('score'),
             'margin': result_json.get('margin'),
             'registration_reference': result_json.get('reg_reference')
             }

    try:
        if teststring is not None:
            raise DefaultCredentialsError
        database = firestore.Client()
        database.collection("results").document(
                        reference).collection("game_results").add(dbdict)
        return jsonify({'write OK': True})
    except DefaultCredentialsError:
        return jsonify({'write OK': False})


@app.route('/gethighscores', methods=['POST'])
def gethighscores():
    """
    return the sorted high scores, the ranking and the
    ref to the lowest score
    """
    jsonstring = json.dumps(request.json)
    result_json = json.loads(jsonstring)
    myscore = result_json.get('score')
    teststring = result_json.get('teststring', None)
    database = None

    if teststring is None:
        try:
            database = firestore.Client()
        except DefaultCredentialsError:
            return jsonify({'highscore': False})
    else:
        database = ResultsDatabase(teststring)

    high_scores = database.collection("high_scores").get()

    high_scores_dict = []
    for score in high_scores:
        score_dict = score.to_dict()
        score_dict['reference'] = score.id
        high_scores_dict.append(score_dict)

    sorted_scores = sorted(high_scores_dict, key=lambda k: k['score'],
                           reverse = True)

    ranking = len(sorted_scores)
    lowest_score = 0
    if len(sorted_scores) > 0:
        lowest_score = sorted_scores[-1].get('reference')

    for rank, score in enumerate(sorted_scores):
        if myscore > score.get('score'):
            ranking = rank
            break

    return jsonify({'scores': sorted_scores,
                    'ranking': ranking,
                    'lowest_ref': lowest_score})


@app.route('/addhighscore', methods=['POST'])
def addhighscore():
    """
    add your score to the high scores
    """
    jsonstring = json.dumps(request.json)
    result_json = json.loads(jsonstring)
    docref = result_json.get('docref', 'new score')
    teststring = result_json.get('teststring', None)
    database = None

    if teststring is None:
        try:
            database = firestore.Client()
        except DefaultCredentialsError:
            return jsonify({'scoreOK': False})
    else:
        database = ResultsDatabase(teststring)

    dbdict = {
             'score': result_json.get('score'),
             'name': result_json.get('name'),
             }
    if docref == 'new score':
        database.collection('high_scores').add(dbdict)
    else:
        database.collection('high_scores').document(docref).set(dbdict)

    return jsonify({'scoreOK': True})


@app.route('/correlation', methods=['POST'])
def correlation():
    """
    Takes in 2d array, and does linear fit and correlation for
    each column against the first
    returns slope, intercept and correlation coefficient
    if there are less than 4 data points it returns false.
    """
    results = np.array(request.json)

    if results.shape[0] < 4:
        return jsonify({'success': False})
    try:
        if results.shape[1] < 2:
            return jsonify({'success': False})
    except IndexError:
        return jsonify({'success': False})

    corr_coeffs = []
    x_points = []
    y_points = []
    success = True
    for column in range (1, results.shape[1]):
        try:
            slope, intercept = np.polyfit(results[:,column], results[:,0], 1)
        except (ValueError, np.linalg.LinAlgError):
            return jsonify({'success': False})

        corr_coeff = np.corrcoef(results[:,0], results[:,column])[0, 1]
        if math.isnan(slope) or math.isnan(intercept) or math.isnan(corr_coeff):
            #remove nans to make client code (javascript) easier
            slope = 0.0
            intercept = 0.0
            corr_coeff = 0.0
            success = False

        start_x = np.min(results[:,column])
        end_x = np.max(results[:,column])
        start_y = intercept + slope * start_x
        end_y = intercept + slope * end_x
        x_points.append([start_x, end_x])
        y_points.append([start_y, end_y])
        corr_coeffs.append(corr_coeff)

    returnjson = {'success': success,
                  'corr_coeffs': corr_coeffs,
                  'xs': x_points,
                  'ys': y_points}
    return jsonify(returnjson)


@app.route('/calculatescore', methods=['POST'])
def calculatescore():
    """
    Delegates to sksurgery.alogorithms.score to
    calculate an ablation score.
    """
    jsonstring = json.dumps(request.json)
    ablation = json.loads(jsonstring)

    target_centre = np.array(ablation.get("target"))
    est_target_centre = np.transpose(np.array(ablation.get("est_target")))
    target_radius = ablation.get("target_radius")
    margin = ablation.get("margin")

    score = calculate_score(target_centre, est_target_centre,
                    target_radius, margin)
    return jsonify({'success': True,
                    'score': score})



if __name__ == '__main__':
    app.run(port=5002, threaded=True)
