#!/bin/bash

for x in dummy/*.json; do
  curl -XPOST http://92.39.246.129:9200/object/product/ -d @$x
done



