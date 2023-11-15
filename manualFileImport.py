import psycopg2 as psy
import pandas as pd
import os
import re
import json
import math

def cleanFrame(dFrame):
    dFrame.drop(columns=['CD:Professional Grader - (ID: 27501)', 'Variation details', 'CD:Grade - (ID: 27502)', 'CD:Card Condition - (ID: 40001)', 'eBay Product ID(ePID)', 'Listing site', 'CDA:Certification Number - (ID: 27503)', 'Reserve price', 'P:UPC', 'P:EAN', 'P:ISBN'], inplace=True)
    itms = {}
    f = lambda x: x.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(':','')
    for itm in dFrame.columns:
        itms[itm] = f(itm)
    dFrame.rename(columns=itms, inplace=True)
    dFrame['watchers'] = dFrame[['watchers']].fillna(value=0).astype(int)
    return dFrame

frames = []
for root, dirs, files in os.walk('listingsToImport'):
    for name in files:
        if name.find('.csv') != -1:
            frames.append(cleanFrame(pd.read_csv(root + '/' + name)))

if len(frames) == 0:
    exit(0)

with open('db.cred', 'r') as f:
    cred = json.load(f)
f.close()

conn = psy.connect(
        host='localhost',
        database="listings",
        user="postgres",
        password=cred['secret']
        )

cur = conn.cursor()
tmp_cols = ['bigint', 'char(80)', 'char(50)', 'int', 'text', 'char(15)', 'decimal', 'decimal', 'decimal', 'int', 'int', 'int', 'int', 'date', 'date', 'char(50)', 'int', 'char(50)', 'int', 'text']

cur.execute('create temp table imported (' + ', '.join([x[0] + ' ' + x[1] for x in zip(frames[0].columns, tmp_cols)]) + ');')

for row in frames[0].iterrows():
    line = []
    for x in row[1]:
        if type(x) == float and math.isnan(x):
            line.append('null')
        else:
            line.append('\'' + str(x).replace('\'', '') + '\'')
    cur.execute('insert into imported ( ' + ', '.join([str(x) for x in frames[0].columns]) + ' )  values ( ' + ', '.join(line) + ' );')
cur.execute("select * from imported;")
print(cur.fetchall())
cur.execute('insert into public.items (creationdate, ebay_id) select current_date, item_number from imported;')
