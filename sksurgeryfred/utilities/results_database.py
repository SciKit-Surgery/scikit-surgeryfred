"""Utilities to enable testing of FRED's firestore databases"""

class TestScore():
    """
    stores a name and a score plus implements to_dict for testing
    """
    def __init__(self, name, score, ref):
        """
        :params name:
        :params score:
        """
        self.name = name
        self.score = score
        self.id = ref # pylint: disable=invalid-name

    def to_dict(self):
        """
        returns a dictionary containing name and score
        """
        return {'name' : self.name, 'score' : self.score}

class TestGet():
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
            self.data = [TestScore('Alice', 678, '78627af'),
                         TestScore('bob', 676, '882399j')]

    def __call__(self):
        return self.data


class TestAddSet():
    """
    implements a get function for testing purposes
    """
    def __call__(self, dictionary):
        return "Add OK"


class TestDoc():
    """
    implements a document for testing purposes
    """

    def __init__(self):
        """
        :params teststring: a string to control behaviour
        """
        self.set = TestAddSet()

    def __call__(self, docref):
        return self


class TestCollection():
    """
    A pretend collection for testing purposes
    """
    def __init__(self, teststring):
        """
        :params teststring: a string to control behaviour
        """
        self.get = TestGet(teststring)
        self.add = TestAddSet()
        self.document = TestDoc()

    def __call__(self, collection_string):
        returnvalue = None
        if collection_string == "high_scores":
            returnvalue = self
        return returnvalue


class ResultsDatabase():
    """
    Stands in as a fake database for testing purposes
    """
    def __init__(self, teststring):
        """
        :params teststring: a string to control behaviour
        """
        self.collection = TestCollection(teststring)
