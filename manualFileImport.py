import psycopg2 as psy
import pandas as pd
import os
import re

frames = []
for root, dirs, files in os.walk('listingsToImport'):
    for name in files:
        if name.find('.csv') != -1:
            frames.append(pd.read_csv(root + '/' + name))

if len(frames) == 0:
    exit(0)
print(frames[0].columns)
