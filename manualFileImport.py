import psycopg2 as psy
import pandas as pd
import os
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
    dFrame['format'] = dFrame[['format']] == 'FIXED_PRICE'
    return dFrame

frames = []
deteteList = []
for root, dirs, files in os.walk('listingsToImport'):
    for name in files:
        if name.find('.csv') != -1:
            frames.append(cleanFrame(pd.read_csv(root + '/' + name)))
            deteteList.append(name)

if len(frames) == 0:
    exit(0)

with open('db.cred', 'r') as f:
    cred = json.load(f)
f.close()

#replaces all nans with null strings and wraps
def applyRow(row):
    line = ', '.join(map(lambda x: 'null' if type(x) == float
                           and math.isnan(x) else '\'' +
                           str(x).replace('\'', '') + '\'', row))
    cur.execute('insert into imported ( ' + ', '.join(str(x) for x in row.keys()) + ' )\
            values ( ' + line + ' );')

conn = psy.connect(
        host='localhost',
        database="postgres",
        user="postgres",
        password=cred['secret']
        )

cur = conn.cursor()

#this is a list of tables that is in a file. should probably be
#simply hardcoded into here. Mostly because other tables might
#be included into the database that don't need to be considered
#when importing a csv file
f = open('tables', 'r')
table_names = f.readlines()[0].replace('\n', '').split(', ')
f.close()

#dictionary of what columns in the database are as keys
#values are the dataframe name that ebay provides in the csv
nameToTable = {'eb_id': 'item_number',
'ebay_id': 'item_number',
'watchers': 'watchers',
'quantity': 'available_quantity',
'current': 'current_price',
'auct_fixed': 'auction_buy_it_now_price',
'format': 'format',
'auct_start': 'start_price',
'bids': 'bids',
'views': 'views_future',
'title': 'title',
'location': 'custom_label_sku',
'creationdate': 'current_date',
'start_date': 'start_date',
'end_date': 'end_date',
'date': 'current_date',
'cat_1_name': 'ebay_category_1_name',
'cat_1_num': 'ebay_category_1_number',
'cat_2_name': 'ebay_category_2_name',
'cat_2_num': 'ebay_category_2_number'}

#this creates a dictionary that maps column names to numbers for use in a tuple
n = 0
colNameToArray = {}
for colNam in frames[0].columns:
    colNameToArray[colNam] = n
    n += 1

#maps all the column names and types into dictionaries
columns = {}
dataTypes = {}
for name in table_names:
    cur.execute('select column_name from information_schema.columns where table_schema = \'public\' and table_name = \'' + name + '\';')
    column = cur.fetchall()
    columns[name] = [x[0] for x in column]
    cur.execute('select data_type from information_schema.columns where table_schema = \'public\' and table_name = \'' + name + '\';')
    dType = cur.fetchall()
    dataTypes[name] = [x[0] for x in dType]

tmp_cols = ['bigint', 'char(80)', 'char(50)', 'int', 'text', 'char(15)', 'decimal', 'decimal', 'decimal', 'int', 'int', 'int', 'int', 'date', 'date', 'char(50)', 'int', 'char(50)', 'int', 'text']

#this function wraps data nicely for the postgres values function
def clean(data, dtype):
    if data == None:
        return 'null'
    if str(dtype) == 'ARRAY':
        return 'array[' + str(data) + ']'
    if data == 'current_date':
        return data
    return '\'' + str(data) + '\''

for frame in frames:
    cur.execute('drop table if exists imported;')
    cur.execute('create temporary table imported (' + ', '.join([x[0] + ' ' + x[1] for x in zip(frame.columns, tmp_cols)]) + ');')

    #I should be able to do this without inserting into the table at all
    frame.apply(lambda x: applyRow(x), axis=1)
    cur.execute('select * from imported;')
    toBeImported = cur.fetchall()

    for imp in toBeImported:
        for name in table_names:
            kols = columns[name][1:]
            highNames = [nameToTable[x] for x in kols]
            impNames = [imp[colNameToArray[x]] if x != 'current_date' else x for x in highNames]
            impFin = [clean(x[0], x[1]) for x in zip(impNames, dataTypes[name][1:])]
            cur.execute('insert into public.' + name + ' ( ' +
                    ', '.join(kols) + ' ) values ( ' + ', '.join(impFin) + ' );')
        conn.commit()


exit(0)

#notes:
# insert item slices into each permanent table. done!
# if an ebay id already exists, you'll want to insert into most of the tables anyways because some of the info
# need to do this one and test with an existing line in the permanent tables
# will usually be different. you'll need to ignore items that already exist in the items table. up next!
# cleanup items that seem to have a zero quantity when queried from the API. to be implemented when I get to actually querying the API.
# might need to either move sold items out of the items table and into a sold table with a similar structure
