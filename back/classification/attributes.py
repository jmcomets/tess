import cPickle as pickle
from sklearn import linear_model

class Classifier(object):
    """
    Low-level classifier using sklearn to built machine learning
    from an input of labeled objects. Takes N attributes defining
    the model used for the machine learning
    """
    def __init__(self, attributes):
        super(Classifier, self).__init__()
        self.learned = False
        self.attributes = attributes
        self.clf = linear_model.BayesianRidge() # TODO add different methods

    def learn(self, matrix, labels):
        """
        Teach the Classifier about a dataset, where matrix/labels
        are both of width/length N.
        """
        self.matrix = matrix
        self.labels = labels
        self.clf.fit(self.matrix, self.labels)
        self.learned = True

    def predict(self, attr_scores):
        """
        Make a prediction based on the scores of the different attributes
        handled by our Classifier (which can be accessed via the attributes
        property).
        """
        prediction = self.clf.predict(attr_scores)
        # TODO do something to format the prediction (round to nearest ?)
        print prediction
        return prediction

def dump_classifier(cls, file_):
    """
    Dump a Classifier which has already learned to a text file.
    """
    assert cls.learned, 'Classifier must learn before being dumped'
    if isinstance(file_, str):
        with open(file_, 'r') as fp:
            pickle.dump(cls, fp)
    else:
        pickle.dump(cls, file_)

def load_classifier(file_):
    """
    Load a Classifier from a given text file.
    """
    if isinstance(file_, str):
        with open(file_, 'r') as fp:
            cls = pickle.load(fp)
    else:
        cls = pickle.load(file_)
    assert isinstance(cls, Classifier)
    cls.learned = True
    return cls
