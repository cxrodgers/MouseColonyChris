# Copy from parent db to this one
import pandas
import sqlite3
import sqlalchemy
import colony.models

#~ conn = sqlite3.connect('../MouseColony/db.sqlite3')
conn = sqlalchemy.create_engine('sqlite:///../MouseColony/db.sqlite3')
mice = pandas.read_sql_table('colony_mouse', conn)
#~ mouse = pandas.read_sql_query("SELECT * FROM colony_mouse WHERE name='1101-1';", conn)
mouse = mice[mice.notes == 'KM86']

new_mouse = colony.models.Mouse()

for colname in mice.columns:
    if colname == 'id':# or colname.endswith('_id'):
        continue
    value = mice.loc[mouse.index[0], colname]
    if pandas.isnull(value):
        continue
    new_mouse.__setattr__(colname, value)

new_mouse.save()