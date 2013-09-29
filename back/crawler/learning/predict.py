import csv
import bisect
import pickle
import itertools as it
from sklearn import linear_model

__all__ = ('Classifier', 'Predictor', 'classify')

pickle_file = 'learning/predictor.txt'

_global_predictor = None
_global_attributes = None
def make_prediction(attr_scores):
    global _global_predictor
    if _global_predictor is None:
        with open(pickle_file, 'r') as fp:
            _global_predictor = Predictor.from_file(fp)
    formatted_attrs = []
    global _global_attributes
    if _global_attributes is None:
        _global_attributes = list(get_headers())
    for attr in _global_attributes:
        found = False
        for attr_, score in attr_scores:
            if attr == attr_:
                formatted_attrs.append(score)
                found = True
                break
        if not found:
            formatted_attrs.append(0)
    assert len(formatted_attrs) == len(_global_attributes)
    return _global_predictor.predict(formatted_attrs)[0]

class Classifier(object):
    def __init__(self):
        super(Classifier, self).__init__()
        self.learned = False

    def learn(self, attributes, data):
        self.attributes = attributes
        data = format_data(attributes, data)
        self.matrix = data['matrix']
        self.labels = data['labels']
        self.pages = data['pages']
        clf = linear_model.BayesianRidge()
        clf.fit(self.matrix, self.labels)
        self.clf = clf
        self.learned = True

    def dump(self, fp):
        pickle.dump(self.clf, fp)

class Predictor(object):
    YES_NO_BOUNDARY = 0.5

    def __init__(self, classifier):
        assert classifier.learned, 'Predictor must learn first!'
        self.cls = classifier

    def predict(self, attr_scores):
        prediction = self.cls.clf.predict(attr_scores)
        try:
            iter(prediction)
        except TypeError:
            prediction = [prediction]
        return [self.YES_NO_BOUNDARY < x for x in prediction]

    @classmethod
    def from_file(self, fp):
        cls = Classifier()
        cls.clf = pickle.load(fp)
        cls.learned = True
        return Predictor(cls)

def get_headers(fp=None):
    if fp is None:
        fp = open('learning/headers.txt', 'r')
    delimiter = '\n'
    return it.ifilter(None, fp.read().strip('\r\n').split(delimiter))

def get_data(attributes, fp=None):
    if fp is None:
        fp = open('learning/data.csv', 'r')
    # read data from file
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        page_data = {
                'page': row.pop(0),
                'product': int(row.pop(0)),
                'attributes': [],
                }
        for attr_score in row:
            attr, score = attr_score.split(':')
            if attr in attributes:
                page_data['attributes'].append({
                    'name': attr,
                    'score': int(score),
                    })
        yield page_data

def format_data(attributes, data):
    # format data to matrix/labels/etc
    pages = []
    labels = []
    matrix = [] # TODO numpy 2D-array
    for page_data in data:
        row = [0] * len(attributes) # TODO numpy 1D-array
        for attr in page_data['attributes']:
            index = attributes.index(attr['name'])
            row[index] = attr['score']
        pages.append(page_data['page'])
        matrix.append(row)
        labels.append(page_data['product'])
    return {
            'matrix': matrix,
            'labels': labels,
            'pages': pages,
            }

def five_fold_cross_validation(attributes, data):
    # five fold cross validation
    import random
    for _ in xrange(5):
        test_size = len(data) / 5
        random.shuffle(data)

        cls = Classifier()
        cls.learn(attributes, data)
        predictor = Predictor(cls)
        test_data = format_data(attributes, data[:test_size])
        test_cases = test_data['matrix']
        labels = test_data['labels']
        pages = test_data['pages']
        predictions = predictor.predict(test_cases)

        # compute recall/precision
        count = lambda ls: sum(it.imap(float, ls))
        intersect = lambda a, b: it.imap(lambda x: x[0] and x[1], it.izip(a, b))
        labeled_yes = predictions
        real_yes = labels
        yes_ok_intersect = intersect(labeled_yes, real_yes)
        yes_ok = count(yes_ok_intersect)
        recall = yes_ok / count(real_yes)
        print 'recall =', yes_ok, '/', count(real_yes), '=', recall
        precision = yes_ok / count(labeled_yes)
        print 'precision =', yes_ok, '/', count(labeled_yes), '=', precision

def run_and_save(attributes, data):
    cls = Classifier()
    cls.learn(attributes, data)
    with open(pickle_file, 'w') as fp:
        cls.dump(fp)

if __name__ == '__main__':
    # load data
    attributes = list(get_headers())
    assert sorted(attributes)
    data = list(get_data(attributes))

    import sys
    if '--test' in sys.argv:
        five_fold_cross_validation(attributes, data)
    else:
        run_and_save(attributes, data)
