import os
from attributes import Classifier, load_classifier, dump_classifier

_this_dir = os.path.dirname(os.path.abspath(__file__))
pickle_file = os.path.join(_this_dir, 'predictor.txt')

_classifier = None
def guess(attr_scores):
    """
    Encapsulation of the load/predict procedure, using a global
    classifier object (saved via a pickle file).
    """

    # Lazy loading of classifier
    global _classifier
    if _classifier is None:
        _classifier = load_classifier(pickle_file)

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

    return _classifier.predict(formatted_attrs)[0]

def index(attributes, data):
    """
    Run the classification indexing based on the
    given attributes/data.
    """
    cls = Classifier(attributes)
    cls.learn(**data)
    with open(pickle_file, 'w') as fp:
        dump_classifier(cls, fp)
