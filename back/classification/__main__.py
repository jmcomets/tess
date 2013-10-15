#!/usr/bin/env python

import sys
import argparse
from __init__ import index
from test import five_fold_cross_validation
from formatting import get_data, get_attributes, format_data

# important data
attributes = get_attributes()
assert sorted(attributes), 'Headers must be sorted in dataset'
data = get_data(attributes)
fmt_data = format_data(attributes, data)

# main argument parser
parser = argparse.ArgumentParser(description=('Multi-use script allowing both'
    'generating and testing the classification.'))
subparsers = parser.add_subparsers()

# "test" argument parser
test_parser = subparsers.add_parser('test', help='test classification based on all available datasets')
def run_test():
    """
    Test action, run to test the classification procedure based
    on a five fold cross validation.
    """
    five_fold_cross_validation(attributes, data)
test_parser.set_defaults(func=run_test)

# "index" argument parser
index_parser = subparsers.add_parser('index', help='index classification based on all available datasets')
def run_index():
    """
    Indexing action, run to index the default (global) classificator.
    """
    index(attributes, fmt_data)
index_parser.set_defaults(func=run_index)

# run program
parsed_args = parser.parse_args()
parsed_args.func()
