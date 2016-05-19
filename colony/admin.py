from django.contrib import admin
from .models import (ChrisMouse, ChrisGenotype, ChrisCage,)
# Register your models here.
from django.db.models import Count
import nested_inline.admin


class ChrisCageAdmin(nested_inline.admin.NestedModelAdmin):
    list_display = ('name',)# 'infos',)
    #~ list_editable = ('notes', )
    
    #~ list_filter = ('proprietor__name',)# DefunctFilter,)
    
    #~ ordering = ('defunct', 'proprietor', 'name',)
    #~ readonly_fields = ('infos', 'needs', 'need_date',)

class ChrisMouseAdmin(admin.ModelAdmin):
    # This controls the columns that show up on the Admin page for Mouse
    list_display = ('name', 'training_name', 'headplate_color', 
        'dob', 'sex', 'cage', 'genotype', )# 'litter', 'notes')
    #~ list_editable = ('notes',)
    #~ readonly_fields = ('info', 'age', 'dob', 'mother', 'father', 'sacked',)
    #~ list_display_links = ('name', 'litter', 'cage')
    #~ list_filter = ['genotype__name', 'breeder',]# SackFilter]

class ChrisGenotypeAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(ChrisMouse, ChrisMouseAdmin)
admin.site.register(ChrisGenotype, ChrisGenotypeAdmin)
admin.site.register(ChrisCage, ChrisCageAdmin)
