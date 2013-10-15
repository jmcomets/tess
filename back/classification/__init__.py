import os
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
        self.clf = linear_model.LinearRegression() # TODO add different methods

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
        return self.clf.predict(attr_scores)

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

_this_dir = os.path.dirname(os.path.abspath(__file__))
pickle_file = os.path.join(_this_dir, 'predictor.txt')

_classifier = None
def guess(attr_scores):
    """
    Encapsulation of the load/predict procedure, using a global
    classifier object (saved via a pickle file).
    """
    # Lazy loading of classifier (~Singleton)
    global _classifier
    if _classifier is None:
        try:
            _classifier = load_classifier(pickle_file)
        except IOError:
            raise AssertionError('Classifier hasn\'t learned anything yet')

    # TODO write using FP
    formatted_attrs = []
    for attr in _classifier.attributes:
        found = False
        for attr_, score in attr_scores:
            if attr == attr_:
                formatted_attrs.append(score)
                found = True
                break
        if not found:
            formatted_attrs.append(0)

    prediction = _classifier.predict([formatted_attrs])[0]
    return prediction

def index(attributes, data):
    """
    Run the classification indexing based on the
    given attributes/data.
    """
    cls = Classifier(attributes)
    cls.learn(**data)
    with open(pickle_file, 'w') as fp:
        dump_classifier(cls, fp)
