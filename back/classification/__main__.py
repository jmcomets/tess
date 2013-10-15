#!/usr/bin/env python

import os
import csv
import sys
import copy
import random
import itertools as it
from __init__ import index, guess, Classifier

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
                'class': int(row.pop(0)),
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
        labels.append(page_data['class'])
    return {
            'matrix': matrix,
            'labels': labels,
            }

def five_fold_cross_validations(attributes, raw_data):
    """
    Validation of the machine learning, using the five
    fold cross validation technique.
    """
    assert isinstance(raw_data, (list, tuple))

    # don't harm the initial dataset
    raw_test_data = copy.deepcopy(raw_data)
    test_size = len(raw_test_data) / 5

    for _ in xrange(5):
        # shuffle the dataset
        random.shuffle(raw_test_data)

        # step 1: teach the classifier
        cls = Classifier(attributes)
        learn_data, test_data = map(lambda x: format_data(attributes, x),
                (raw_test_data[:test_size], raw_test_data[test_size:]))
        cls.learn(**learn_data)

        # step 2: check test cases
        predictions = []
        test_cases = test_data['matrix']
        for test_case in test_cases:
            prediction = cls.predict(test_case)
            made_prediction = guess(zip(attributes, test_case))
            #print 'prediction =', prediction
            #print 'made prediction =', made_prediction
            #assert made_prediction is prediction
            predictions.append(prediction)

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
    print 'Five-fold Cross-validation'
    print '--------------------------'
    print
    average_recall = 0
    average_precision = 0
    nb_steps = 0
    ffcv = five_fold_cross_validations
    for step, recall_precision in enumerate(ffcv(attributes, data)):
        recall, precision = recall_precision
        average_recall += recall
        average_precision += precision
        nb_steps += 1
        print '## Step', step
        print
        print '* recall =', recall
        print '* precision =', precision
        print
    average_recall /= nb_steps
    average_precision /= nb_steps
    print '# Summary'
    print
    print '* average recall =', average_recall
    print '* average precision =', average_precision
    #print '# Summary :

# main program

attributes = get_headers()
assert sorted(attributes), 'Headers must be sorted'
data = get_data(attributes)
fmt_data = format_data(attributes, data)

if '--test' in sys.argv:
    test_classification(attributes, data)
else:
    index(attributes, fmt_data)
