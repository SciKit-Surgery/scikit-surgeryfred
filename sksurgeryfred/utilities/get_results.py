"""
Script to download and parse results from firestore
"""

from google.cloud import firestore
from sksurgeryfred.utilities.results_database import ResultsDatabase

def get_results(testing = False):
    """
    Function to download results from our results database and
    parse them ready for analysis
    """
    database = None
    if testing:
        database = ResultsDatabase('empty')
    else:
        database = firestore.Client()

    results=database.collection("results").get()

    for result in results:
        result_dictionary = result.to_dict()
        time = result_dictionary.get('time')
        version = result_dictionary.get('fred verion')
        game_results = result.reference.collection("game_results").get() #pylint: disable=no-member
        for game_result in game_results:

            result_dictionary = game_result.to_dict()
            category = result_dictionary.get('state')
            score = result_dictionary.get('score')
            margin = result_dictionary.get('margin')

            print (time, ', fred version', version, ', ', category,
                            ', ', score, ', ', margin)
