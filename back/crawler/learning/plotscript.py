"""
Demo of the histogram (hist) function with a few features.

In addition to the basic histogram, this demo shows a few optional features:

    * Setting the number of data bins
    * The ``normed`` flag, which normalizes bin heights so that the integral of
      the histogram is 1. The resulting histogram is a probability density.
    * Setting the face color of the bars
    * Setting the opacity (alpha value).

"""
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')

with open('headers.txt') as header_file:
    headers = {header : i for i, header in enumerate(header_file.read().split(','))}


c = Counter()
with open('data.csv') as data_file:
    for line in data_file:

        elements = line.split(',')
        url = elements[0]
        positive = elements[1] == '1'
        for element in elements[2:]:
            header, value = element.split(':')
            if not header in headers:
                continue
            header_id = headers[header]
            c[header_id] += int(value)

values = [ i[1] for i in sorted(c.items())]


# the histogram of the data
n, bins, patches = plt.hist(values, len(headers), normed=1, facecolor='green', alpha=0.5)
# add a 'best fit' line
plt.plot(values)
plt.xlabel('Labels')
plt.ylabel('Occurences')
plt.title(r'Histogram')

# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)

print 'Saving "{}" graph to PDF...'.format(url)
plt.show()
