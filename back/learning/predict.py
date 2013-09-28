import sys
import csv
import bisect
import itertools
from sklearn import linear_model

def get_headers(filename, delimiter=','):
    with open(filename, 'r') as file_:
        return filter(None, file_.read().strip('\r\n').split(delimiter))

class DataReader:
    def __init__(self, classes):
        assert sorted(classes)
        self.classes = classes
        self.pages = []
        self.matrix = []
        self.labels = []

    def read_data(self, filename):
        data = []
        with open(filename, 'r') as file_:
            reader = csv.reader(file_, delimiter=';')
            for row in reader:
                page_data = {
                        'page': row.pop(0),
                        'product': bool(int(row.pop(0))),
                        'classes': [],
                        }
                for i in xrange(0, len(row), 2):
                    class_, score = row[i:i+2]
                    assert class_ in self.classes, '%s not in known classes %s' % (class_, self.classes)
                    page_data['classes'].append({
                        'name': class_,
                        'score': int(score),
                        })
                data.append(page_data)
        self.add_data(data)

    def add_data(self, data):
        # TODO switch to numpy array
        for page_data in data:
            row = [0] * len(self.classes)
            for class_ in page_data['classes']:
                index = bisect.bisect_left(self.classes, class_['name'])
                row[index] = class_['score']
            self.pages.append(page_data['page'])
            self.matrix.append(row)
            self.labels.append(page_data['product'])

def read_data(classes, filename):
    dr = DataReader(classes)
    dr.read_data(filename)
    return {
            'matrix': dr.matrix,
            'labels': dr.labels,
            'pages': dr.pages,
            }
classes = get_headers('headers.txt', delimiter=',')
data = read_data(classes, 'sample.txt')
clf = linear_model.BayesianRidge()
clf.fit(data['matrix'], data['labels'])
test_cases = list(itertools.product(range(2), repeat=3))
print 'Matrix:'
for i, row in enumerate(data['matrix']):
    print row, '->', data['labels'][i]
print
print 'Predictions:'
predictions = [0.5 < x for x in clf.predict(list(test_cases))]
for test_case, prediction in itertools.izip(test_cases, predictions):
    print test_case, '->', prediction
