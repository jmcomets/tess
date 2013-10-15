#!/usr/bin/env python

import os
import csv
import sys
import itertools as it
from attributes import Classifier, dump_classifier

_this_dir = os.path.dirname(os.path.abspath(__file__))
headers_file = os.path.join(_this_dir, 'headers.txt')
data_file = os.path.join(_this_dir, 'data.csv')

def get_headers(fp=None):
    if fp is None:
        fp = open(headers_file, 'r')
    delimiter = '\n'
    return filter(None, fp.read().strip('\r\n').split(delimiter))

def get_data(attributes, fp=None):
    if fp is None:
        fp = open(data_file, 'r')
    # read data from file
    all_page_data = []
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        page_data = {
                'page': row.pop(0), # FIXME: not used (for now)
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
        all_page_data.append(page_data)
    return all_page_data

def format_data(attributes, data):
    """
    Format page data to matrix/labels/etc...
    """
    labels = []
    matrix = [] # TODO numpy 2D-array
    for page_data in data:
        row = [0] * len(attributes) # TODO numpy 1D-array
        for attr in page_data['attributes']:
            index = attributes.index(attr['name'])
            row[index] = attr['score']
        matrix.append(row)
        labels.append(page_data['product'])
    return {
            'matrix': matrix,
            'labels': labels,
            }

def run_and_index(attributes, data):
    """
    Run the classification indexing based on the
    given attributes/data.
    """
    cls = Classifier(attributes)
    fmt_data = format_data(attributes, data)
    cls.learn(**fmt_data)
    with open(pickle_file, 'w') as fp:
        dump_classifier(cls, fp)

def five_fold_cross_validations(attributes, data):
    """
    Validation of the machine learning, using the five
    fold cross validation technique.
    """
    import random
    for _ in xrange(5):
        # shuffle the dataset
        random.shuffle(data)

        # step 1: teach the classifier
        cls = Classifier(attributes)
        fmt_data = format_data(attributes, data)
        test_size = len(data) / 5
        learn_data, test_data = fmt_data[:test_size], fmt_data[test_size:]
        cls.learn(attributes, **learn_data)

        # step 2: check test cases
        test_cases = test_data['matrix']
        predictions = cls.predict(test_cases)
        for prediction, test_case in it.izip(predictions, test_cases):
            attributes_tuples = zip(attributes, test_case)
            made_prediction = make_prediction(attributes_tuples)
            assert made_prediction is prediction

        # compute recall/precision
        count = lambda ls: sum(it.imap(float, ls))
        intersect = lambda a, b: it.imap(lambda x: x[0] and x[1], it.izip(a, b))
        labeled_yes = predictions
        real_yes = test_data['labels']
        yes_ok_intersect = intersect(labeled_yes, real_yes)
        yes_ok = count(yes_ok_intersect)
        recall = yes_ok / count(real_yes)
        precision = yes_ok / count(labeled_yes)

        # yield recall/precision
        yield recall, precision

def test_classification(attributes, data):
    ffcv = five_fold_cross_validations
    print 'Five-fold Cross-validation'
    for step, recall_precision in enumerate(ffcv(attributes, data)):
        recall, precision = recall_precision
        print '- step', step
        print '  - recall', recall
        print '  - precision', precision

# main program

attributes = get_headers()
assert sorted(attributes), 'Headers must be sorted'
data = get_data(attributes)
data = format_data(attributes, data)

if '--test' in sys.argv:
    test_classification(attributes, data)
else:
    run_and_index(attributes, data)
