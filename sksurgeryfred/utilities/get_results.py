#Script to download and parse results from firestore

from google.cloud import firestore

database = firestore.Client()

results=database.collection("results").get()

for result in results:
    print (result.to_dict())
    game_results = result.reference.collection("game_results").get()
    for game_result in game_results:
        print (game_result.to_dict())

