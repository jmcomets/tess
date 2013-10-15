import pickle # TODO cPickle ?
from sklearn import linear_model

class Classifier(object):
    """
    Low-level classifier using sklearn to built machine learning
    from an input of labeled objects.
    """
    def __init__(self, attributes):
        super(Classifier, self).__init__()
        self.learned = False
        self.attributes = attributes

    def learn(self, matrix, labels):
        self.matrix = matrix
        self.labels = labels
        clf = linear_model.BayesianRidge()
        clf.fit(self.matrix, self.labels)
        self.clf = clf
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
            pickle.dump(cls.clf, fp)
    else:
        pickle.dump(cls.clf, file_)

def load_classifier(fp):
    """
    Load a Classifier from a given text file.
    """
    cls = Classifier()
    cls.clf = pickle.load(fp)
    cls.learned = True
    return cls
