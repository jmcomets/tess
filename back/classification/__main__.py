#!/usr/bin/env python

import copy
import random
import argparse
import itertools as it
from __init__ import index, guess, Classifier
from classifier_format import get_data, get_attributes, format_data

def five_fold_cross_validations(attributes, raw_data):
    """
    Validation of the machine learning, using the five
    fold cross validation technique.
    Generates (recall, precision) tuples.
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

# argument parser
parser = argparse.ArgumentParser(description=('Multi-use script allowing both'
    'generating and testing the classification.'))
parser.add_argument('--test', action='store_true',
        help='test the classification based on all available datasets')
parsed_args = parser.parse_args()

# important data
attributes = get_attributes()
assert sorted(attributes), 'Headers must be sorted in dataset'
data = get_data(attributes)
fmt_data = format_data(attributes, data)

if parsed_args.test:
    test_classification(attributes, data)
else:
    index(attributes, fmt_data)
