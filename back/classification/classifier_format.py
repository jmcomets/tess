import os
import csv
import copy

_this_dir = os.path.dirname(os.path.abspath(__file__))
headers_file = os.path.join(_this_dir, 'headers.txt')
data_file = os.path.join(_this_dir, 'data.csv')

def get_attributes(fp=None):
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
