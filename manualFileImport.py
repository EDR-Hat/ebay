import psycopg2 as psy
import pandas as pd
import os
import re
import json

def cleanFrame(dFrame):
    dFrame.drop(columns=['CD:Professional Grader - (ID: 27501)', 'Variation details', 'CD:Grade - (ID: 27502)', 'CD:Card Condition - (ID: 40001)', 'eBay Product ID(ePID)', 'Listing site', 'CDA:Certification Number - (ID: 27503)', 'Reserve price'], inplace=True)
    itms = {}
    f = lambda x: x.lower().replace(' ', '_').replace('(', '').replace(')', '')
    for itm in dFrame.columns:
        itms[itm] = f(itm)
    dFrame.rename(columns=itms, inplace=True)
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
tmp_cols = ['bigint', 'varchar(80)', 'varchar(50)', 'int', 'varchar(10)', 'varchar(15)', 'decimal', 'decimal', 'decimal', 'int', 'int', 'int', 'int', 'date', 'date', 'varchar(50)', 'int', 'varchar(50)', 'int', 'varchar(20)', 'bigint', 'bigint', 'bigint']

#cur.execute('create temp table test (' + ', '.join([x[0] + ' ' + x[1] for x in zip(tmp_cols, frames[0].columns)]) + ');')
cur.execute('create temp table test ( ' + ', '.join([x[0] + ' ' + x[1] for x in zip(tmp_cols, frames[0].columns)]) + ' );')
