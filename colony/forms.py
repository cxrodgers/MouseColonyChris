from django.forms import formsets
from django.forms.models import BaseInlineFormSet

# This works for statically filling info but I can't make it dynamically
# use the info from the cage
#~ class MouseFormSet(BaseInlineFormSet):
    #~ def __init__(self, *args, **kwargs):
        #~ super(MouseFormSet, self).__init__(*args, **kwargs)
        #~ # Check that the data doesn't already exist
        #~ if True: #not kwargs['instance'].member_id_set.filter(# some criteria):
            #~ initial = []
            #~ initial.append({'father': 'Chris'}) # Fill in with some data
            #~ self.initial = initial
            #~ # Make enough extra formsets to hold initial forms
            #~ self.extra += len(initial)

