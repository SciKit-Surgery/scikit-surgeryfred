"""Utilities to enable testing of FRED's firestore databases"""

class test_score():
    """
    stores a name and a score plus implements to_dict for testing
    """
    def __init__(self, name, score, ref):
        """
        :params name:
        :params score:
        """
        self.name = name;
        self.score = score;
        self.id = ref

    def to_dict(self):
        """
        returns a dictionary containing name and score
        """
        return {'name' : self.name, 'score' : self.score}

class test_get():
    """
    implements a get function for testing purposes
    """
    def __init__(self, teststring):
        """
        :params teststring: a string to control behaviour
        """
        if teststring == 'empty':
            self.data = []
        else:
            self.data = [test_score('Alice', 678, '78627af'), 
                         test_score('bob', 676, '882399j')]

    def __call__(self):
        return self.data

class test_collection():
    """
    A pretend collection for testing purposes
    """
    def __init__(self, teststring):
        """
        :params teststring: a string to control behaviour
        """
        self.get = test_get(teststring)

    def __call__(self, collection_string):
        if collection_string == "high_scores":
            return self


class results_database():
    """
    Stands in as a fake database for testing purposes
    """
    def __init__(self, teststring):
        """
        :params teststring: a string to control behaviour
        """
        self.collection = test_collection(teststring)
