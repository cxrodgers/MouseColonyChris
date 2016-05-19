# This needs to be run in django shell
# Copy a mouse from the master database to ChrisMouseColony
import pandas
import sqlalchemy
import colony.models
import os

# Which mouse to get and what info to assign
target_mouse_name = 'CR27-1'
headplate_color = 'GB'
training_name = 'KM86'

# Connect to the master database
# Should be a way to get this using the django ORM and specifying which one
database_path = os.path.expanduser('~/mnt/django/MouseColony/db.sqlite3')
if not os.path.exists(database_path):
    raise IOError("cannot find database: %s" % database_path)
conn = sqlalchemy.create_engine('sqlite:///%s' % database_path)

# Read the tables using pandas
mouse_table = pandas.read_sql_table('colony_mouse', conn)
genotype_table = pandas.read_sql_table('colony_genotype', conn).set_index('id')

# Identify the row that corresponds to the target mouse
# This should actually be done by the name not the notes
mouse = mouse_table[mouse_table.name == target_mouse_name].iloc[0]

# Check whether this mouse is already in the database
if len(colony.models.ChrisMouse.objects.filter(name=mouse['name'])) > 0:
    raise ValueError("Mouse with that name already exists")

# Create a new mouse with values copied from the old one
new_mouse = colony.models.ChrisMouse()
new_mouse.name = mouse['name']
new_mouse.sex = mouse.sex

if not pandas.isnull(mouse.litter_id):
    raise ValueError("I don't know how to get dob from litter yet")
elif not pandas.isnull(mouse.manual_dob):
    new_mouse.dob = mouse.manual_dob
else:
    print "warning: cannot get dob"

# Specified values
new_mouse.training_name = training_name
new_mouse.headplate_color = headplate_color

# Try to find matching genotype
genotype_name = genotype_table.loc[mouse.genotype_id, 'name']
matching_genotypes = colony.models.ChrisGenotype.objects.filter(
    name=genotype_name)
if len(matching_genotypes) == 0:
    # Create a new one
    new_genotype = colony.models.ChrisGenotype(name=genotype_name)
    new_genotype.save()
elif len(matching_genotypes) == 1:
    new_genotype = matching_genotypes[0]
else:
    raise ValueError("too many matching genotypes")

# Set the genotype
new_mouse.genotype = new_genotype

new_mouse.save()