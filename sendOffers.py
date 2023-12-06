import psycopg2 as psy
import pandas as pd
import os
import json
import math


with open('db.cred', 'r') as f:
    cred = json.load(f)
f.close()

conn = psy.connect(
        host='localhost',
        database="postgres",
        user="postgres",
        password=cred['secret']
        )

cur = conn.cursor()

#define how to format directives CSV might be best
#load line from offer directives
#load api token
#request eligible item ids
#error check request response
#for each item id, follow the offer directive based on its settings
# -this might mean grabbing the price and time data for that item in the local database
# -basic directive should take into account time first listed, current price and initial price
