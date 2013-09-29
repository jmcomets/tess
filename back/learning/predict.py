import csv
import bisect
from sklearn import linear_model

__all__ = ('Predictor')

class Predictor(object):
    def __init__(self):
        super(Predictor, self).__init__()
        self.learned = False

    def learn(self, headers_file, data_file):
        self.attributes = get_headers(headers_file)
        data = get_data(self.attributes, data_file)
        self.matrix = data['matrix']
        self.labels = data['labels']
        self.pages = data['pages']
        clf = linear_model.BayesianRidge()
        clf.fit(self.matrix, self.labels)
        self.clf = clf
        self.learned = True

    def predict(self, attr_scores):
        assert self.learned, 'Predictor must learn first!'
        return 0.5 < self.clf.predict(attr_scores)

def get_headers(filename):
    delimiter = ','
    with open(filename, 'r') as file_:
        return filter(None, file_.read().strip('\r\n').split(delimiter))

def get_data(attributes, filename):
    assert sorted(attributes)
    # read data from file
    data = []
    with open(filename, 'r') as file_:
        reader = csv.reader(file_, delimiter=',')
        for row in reader:
            page_data = {
                    'page': row.pop(0),
                    'product': bool(int(row.pop(0))),
                    'attributes': [],
                    }
            for attr_score in row:
                attr, score = attr_score.split(':')
                assert attr in attributes
                page_data['attributes'].append({
                    'name': attr,
                    'score': int(score),
                    })
            data.append(page_data)

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
    import itertools
    predictor = Predictor()
    predictor.learn('headers.txt', 'data.csv')
    test_data = get_data(predictor.attributes, 'data-test.csv')
    test_cases = test_data['matrix']
    labels = test_data['labels']
    pages = test_data['pages']
    predictions = [x for x in predictor.predict(test_cases)]
    # compute recall/precision
    count = lambda ls: sum(itertools.imap(float, ls))
    intersect = lambda a, b: itertools.imap(lambda x: x[0] and x[1], itertools.izip(a, b))
    intersect
    labeled_yes = predictions
    real_yes = labels
    recall = count(intersect(labeled_yes, real_yes)) / count(real_yes)
    precision = count(intersect(labeled_yes, real_yes)) / count(labeled_yes)
    print 'recall =', recall
    print 'precision =', precision
