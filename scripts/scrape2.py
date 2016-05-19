# Legacy version to copy mice from my old django to my new one

# This needs to be run in django shell
# Copy a mouse from the master database to ChrisMouseColony
import pandas
import sqlalchemy
import colony.models
import os

# Which mouse to get and what info to assign
training_names_to_copy = ['KF74', 'KF76', 'KF77', 'KF78']
cage_name = 'Reserve F'

# Connect to the master database
# Should be a way to get this using the django ORM and specifying which one
database_path = os.path.expanduser('~/mnt/marvin/django/mouse/db.sqlite3')
if not os.path.exists(database_path):
    raise IOError("cannot find database: %s" % database_path)
conn = sqlalchemy.create_engine('sqlite:///%s' % database_path)

# Read the tables using pandas
mouse_table = pandas.read_sql_table('colony_mouse', conn)
genotype_table = pandas.read_sql_table('colony_genotype', conn).set_index('id')
litter_table = pandas.read_sql_table('colony_litter', conn).set_index('id')

# Identify the row that corresponds to the target mouse
# This should actually be done by the name not the notes
for idx in mouse_table[mouse_table.training_name.isin(
    training_names_to_copy)].index:

    # Check whether this mouse is already in the database
    if len(colony.models.ChrisMouse.objects.filter(
        name=mouse_table.loc[idx, 'name'])) > 0:
        print "skipping mouse %s, already exists" % mouse_table.loc[idx, 'name']
        continue
        #~ raise ValueError("Mouse with that name already exists")

    # Create a new mouse with values copied from the old one
    new_mouse = colony.models.ChrisMouse()
    new_mouse.name = mouse_table.loc[idx, 'name']
    new_mouse.sex = mouse_table.loc[idx, 'sex']

    if not pandas.isnull(mouse_table.loc[idx, 'litter_id']):
        new_mouse.dob = litter_table.ix[
            int(mouse_table.loc[idx, 'litter_id'])].dob
    elif not pandas.isnull(mouse_table.loc[idx, 'dob']):
        new_mouse.dob = mouse_table.loc[idx, 'dob']
    else:
        print "warning: cannot get dob"

    # Specified values
    new_mouse.training_name = mouse_table.loc[idx, 'training_name']
    new_mouse.headplate_color = mouse_table.loc[idx, 'headplate_color']

    # Try to find matching genotype
    genotype_name = genotype_table.loc[
        mouse_table.loc[idx, 'genotype_id'], 'name']
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
    new_mouse.genotype = new_genotype

    # Try to find matching cage
    matching_cages = colony.models.ChrisCage.objects.filter(
        name=cage_name)
    if len(matching_cages) == 0:
        # Create a new one
        new_cage = colony.models.ChrisCage(name=cage_name)
        new_cage.save()
    elif len(matching_cages) == 1:
        new_cage = matching_cages[0]
    else:
        raise ValueError("too many matching cages")
    new_mouse.cage = new_cage
    
    new_mouse.save()