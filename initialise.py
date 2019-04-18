### Example inspired by Tutorial at https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
### However the actual example uses sqlalchemy which uses Object Relational Mapper, which are not covered in this course. I have instead used natural sQL queries for this demo. 
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, BlogForm
import pandas as pd
import numpy as np
import sqlite3
import scrape
import datetime
import random

conn = sqlite3.connect('survivor.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# get a list of contestants
SERIES_URL = 'https://en.wikipedia.org/wiki/Survivor_(U.S._TV_series)'
ROOT_URL = 'https://en.wikipedia.org'

# get the seasons from the series
seasons = scrape.WikiTable(url= SERIES_URL,
                        table_class='wikitable',
                        columns=['Season title'],
                        cell_details=dict(attributes=['href'],
                                          elements=['a'])).df

# get the latest season contestants
latest = seasons.iloc[-1]['Season title']
target_url = ROOT_URL + latest

# table class
tclass = 'wikitable sortable'

# get the contestants
cons = scrape.WikiTable(url=target_url,
                            table_class=tclass,
                            columns=['Contestant', 'Voted out']).df

# strip the text
for col in cons.columns:
    cons.loc[:, col] = cons[col].str.strip()

cons['Voted out'] = cons['Voted out'].str.split('Day', expand=True)[0].str[:-2].str.strip()
cons['Voted out'] = cons['Voted out'].apply(lambda x: int(x) if len(x)>0 else None)
cons = cons.sort_values(['Voted out'])

# print('Contestants raw:')
# print('\n', cons, '\n')


# first thing we do is drop any row that has "returned"
to_drop = cons['Contestant'].str.lower().str.contains('returned')
cons = cons[~to_drop]

# break up the data in the first row into, first_name, last_name, age, origin
# - split on age - assuming two numbers
temp = cons['Contestant'].str.split('(?=[0-9]{2})', expand=True).dropna(how='any')
temp.columns = ['full_name', 'rest']
temp['full_name'] = temp['full_name'].str.strip()
# print('Names and the rest:')
# print(temp.head(), '\n')

# - split on commas
temp1 = temp['rest'].str.split(',', expand=True)
temp1.columns = ['age', 'city', 'state']
# print('Ages, locations and previous seasons:')
# print(temp1.head(), '\n')

# - split in little character followed by a capital
# - these are the row of the returned contestants
retemp = temp1[temp1['state'].str.contains('[a-z][A-Z]', regex=True)]
# print('Match returns:')
# print(retemp.head(), '\n')

# split state and previous seasons
retemp1 = retemp['state'].str.split('(?<=[a-z])(?=[A-Z])', expand=True)
retemp1.columns = ['state', 'previous_seasons']
# print('Split state and previous seasons:')
# print(retemp1.head(), '\n')

# get the previous seasons
retemp2 = retemp1['previous_seasons'].str.split('&', expand=True)
# print('Split up the previous seasons:')
# print(retemp2.head(), '\n')

# stick it all together
firsts = cons.drop(retemp.index).index.values
returns = retemp.index.values
first_timers = temp.loc[firsts].merge(temp1.loc[firsts], left_index=True, right_index=True, how='inner').drop('rest', axis=1)

# # print some stuff
# print('\n', cons, '\n')
# print('\n', temp1, '\n')
# print('\n', retemp1, '\n')
# print('\n', retemp2, '\n')

# join the bits of the returning contestants together
returnings = temp.loc[returns].merge(temp1.loc[returns, ['age', 'city']], left_index=True, right_index=True, how='inner').drop('rest', axis=1)
returnings.loc[returnings.index, 'voted_out'] = cons.loc[returnings.index, 'Voted out']
returnings['state'] = retemp1['state']
returnings = returnings.merge(retemp2, left_index=True, right_index=True, how='inner').reset_index(drop=True)

# get voted out details back for the first timers
first_timers.loc[first_timers.index, 'voted_out'] = cons.loc[first_timers.index, 'Voted out']

# melt the returning seasons (those after the state column)
state_index = list(returnings.columns).index('state')

# increment the returning season column values
rcols = list(returnings.columns)[:state_index+1] + [col + 1 for col in returnings.columns[state_index+1:]]

# convert to string to work in pd.melt
rcols = [str(col) for col in rcols]
returnings.columns = rcols
meltcols = rcols[state_index+1:]

# print('\n', returnings.head(), '\n')

# melt
returnings = pd.melt(
    frame=returnings, 
    id_vars=['full_name', 'age', 'city', 'state', 'voted_out'],
    value_vars=meltcols,
    var_name='num_attempt',
    value_name='season_name'
    ).dropna(how='any').sort_values(['full_name', 'num_attempt']).reset_index(drop=True)

# print('\n', rcols[rcols.index('state')+1:], '\n')
# print('\n', returnings.head(), '\n')

# strip all of the columns
ft0 = first_timers.iloc[0].values
for col, val in zip(first_timers.columns, ft0):
    if type(val) == str:
        first_timers[col] = first_timers[col].str.strip()

# strip all of the columns
r0 = returnings.iloc[0].values
for col, val in zip(returnings.columns, r0):
    if type(val) == str:
        returnings[col] = returnings[col].str.strip()

# now make the contestants table to have name
# print('\n', first_timers.head(), '\n')
# print('\n', returnings.head(), '\n')

# contestants
concols = ['full_name', 'age', 'city', 'state', 'voted_out']
contestants = first_timers.loc[:, concols].append(
    returnings.loc[:, concols]
).drop_duplicates().sort_values(['voted_out', 'full_name']).reset_index(drop=True)
contestants['origin_town'] = contestants['city'] + ', ' + contestants['state']
contestants = contestants.drop(['city', 'state'], axis=1)

# remove quotations from names
contestants['full_name'] = contestants['full_name'].str.replace('"', '')
# print('Contestants:')
# print('\n', contestants, '\n')

'''
HERE WE ARE GOING TO HACK IN SOME DATA FOR THE CONTESTANT AND TEAMS AND THEN PERFORM A QUERY
TO CALCULATE SCORES AND RANK THE PLAYERS
'''
# get data from episodes
print('Scraping Episodes ...')
ep_raw = scrape.WikiTable(url= target_url,
                        table_class='wikitable plainrowheaders nowrap',
                        columns=['Episode title', 'Eliminated'], show_logs=False, header_offset=True).df

# only keep the rows that have quotations at the start
episodes = ep_raw[ep_raw['Episode title'].str[0]=='"'].reset_index(drop=True)
episodes['Episode title'] = episodes['Episode title'].str.strip().str[1:-1]
episodes['Eliminated'] = episodes['Eliminated'].str.strip()
# print('Episodes:')
# print('\n', episodes, '\n')

# clear tables before populating
conn = sqlite3.connect('survivor.db')
c = conn.cursor() 
c.execute("delete from Episode;")
conn.commit()
conn = sqlite3.connect('survivor.db')
c = conn.cursor() 
c.execute("delete from Contestant;")
conn.commit()
conn = sqlite3.connect('survivor.db')
c = conn.cursor() 
c.execute("delete from Based_on;")
conn.commit()

### EPISODES ###
# populate the episode, contestant and teams tables
conn = sqlite3.connect('survivor.db')
c = conn.cursor()
for idx, row in episodes.iterrows():
    # add to the query
    c.execute('INSERT INTO Episode (ep_no, season_no, ep_nm) VALUES ({}, 38, "{}");'.format(int(idx+1), row['Episode title']))
conn.commit()

### CONTESTANTS ### 
# populate the episode, contestant and teams tables
conn = sqlite3.connect('survivor.db')
c = conn.cursor()
for idx, row in contestants.iterrows():
    # add to the query
    epno = int(row['voted_out']) if row['voted_out'] > 0 else 'Null' 
    c.execute('INSERT INTO Contestant (name, age, origin_town, season_no, ep_no)\
         VALUES ("{}", {}, "{}", {}, {});'.format(row['full_name'], row['age'], row['origin_town'], 38, epno))
conn.commit()

### Make the teams ###
# query the teams and then query the contestants
# shuffle the contestants table and take the top four rows to assign as team members

# teams
conn = sqlite3.connect('survivor.db')
conn.row_factory = dict_factory
c = conn.cursor()
c.execute('select * from Team')
teams = pd.DataFrame(c.fetchall())

# contestants
c.execute('select * from Contestant')
condb = pd.DataFrame(c.fetchall())

# go through the teams, shuffle the contestants and take the top 4 as the team members
# then commit these to based_on in the database
conn = sqlite3.connect('survivor.db')
c = conn.cursor()
random.seed(1)
conlist = list(condb['contestant_id'].values)
for t in teams['team_nm']:
    temp = list(conlist)
    random.shuffle(temp)
    members = temp[:4]

    for m in members:
        c.execute('insert into Based_on (team_nm, contestant_id) VALUES ("{}", {});'.format(t, m))
conn.commit()

# teams
conn = sqlite3.connect('survivor.db')
conn.row_factory = dict_factory
c = conn.cursor()
c.execute('select * from Based_on')
based = pd.DataFrame(c.fetchall())

if __name__ == '__main__':
    app.run(debug=True)

