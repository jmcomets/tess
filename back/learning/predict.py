import csv
import bisect
import pickle
import itertools as it
from sklearn import linear_model

__all__ = ('Classifier', 'Predictor')

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

class Predictor(object):
    YES_NO_BOUNDARY = 0.5

    def __init__(self, classifier):
        assert classifier.learned, 'Predictor must learn first!'
        self.cls = classifier

    def predict(self, attr_scores):
        return [self.YES_NO_BOUNDARY < x for x in self.cls.predict(attr_scores)]

    @classmethod
    def from_file(self, fp):
        cls = Classifier()
        cls.clf = pickle.load(fp)
        cls.learned = True
        return Predictor(cls)

    def dump(self, fp):
        pickle.dump(self.cls.clf, fp)

def get_headers(fp):
    delimiter = '\n'
    return it.ifilter(None, fp.read().strip('\r\n').split(delimiter))

def get_data(attributes, fp):
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
            assert attr in attributes
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

if __name__ == '__main__':
    print 'Loading headers...'
    with open('headers.txt', 'r') as fp:
        attributes = list(get_headers(fp))
        assert sorted(attributes)
    print 'Loading data...'
    with open('data.csv', 'r') as fp:
        data = list(get_data(attributes, fp))

    # five fold cross validation
    import random
    for _ in xrange(5):
        test_size = len(data) / 5
        random.shuffle(data)

        print 'Classifying data...'
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
