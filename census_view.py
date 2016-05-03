# Create a CensusView
import colony.models
import pandas



rec_l = []
mouse_df_l = []
for cage in colony.models.Cage.objects.all():
    for mouse in cage.mouse_set.all():
        rec_l.append({
            'cage': cage.name,
            'proprietor': cage.proprietor,
            'mouse': mouse.name,
            'sex': mouse.sex,
            'dob': mouse.dob,
            })
mouse_df = pandas.DataFrame.from_records(rec_l)
mouse_df_print = mouse_df.copy()
mouse_df_print.loc[
    mouse_df.cage == mouse_df.cage.shift(),
    'cage'] = ''
mouse_df_print.loc[
    mouse_df.cage == mouse_df.cage.shift(),
    'proprietor'] = ''

mouse_df_lines = mouse_df_print.to_string(header=False, index=False).split('\n')

for cage, subdf in mouse_df.groupby('cage'):
    for idx in subdf.index:
        print mouse_df_lines[idx]
    print "-----------------------------------------------"

#~ print mouse_df_print.to_string()

1/0
    
    
    



rec_l = []
mouse_df_l = []
for cage in colony.models.Cage.objects.all():
    rec_l.append({
        'name': cage.name,
        'proprietor': cage.proprietor,
        })
    
    mouse_rec_l = []
    for mouse in cage.mouse_set.all():
        mouse_rec_l.append({
            'name': mouse.name,
            'sex': mouse.sex,
            'genotype': mouse.genotype,
            'dob': mouse.dob})
    mouse_df = pandas.DataFrame.from_records(mouse_rec_l)

    mouse_df_l.append(mouse_df)
cage_df = pandas.DataFrame.from_records(rec_l)


cage_df_lines = cage_df.to_string().split('\n')
cage_df_header = cage_df_lines[0]
cage_df_lines = cage_df_lines[1:]

print cage_df_header
for ncage in range(len(cage_df)):
    print cage_df_lines[ncage]
    print mouse_df_l[0].to_string()
    print "\n"
