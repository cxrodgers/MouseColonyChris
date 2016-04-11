from django.contrib import admin
from .models import (Mouse, Genotype, Litter, 
    Cage, Person, Task)
# Register your models here.
from django.db.models import Count
import nested_inline.admin

class MouseInline(nested_inline.admin.NestedTabularInline):
    model = Mouse
    extra = 1
    exclude = ('manual_dob', 'manual_mother', 'manual_father')
    show_change_link = True    
    
    # How can we make "notes" the right-most field?

class LitterInline(nested_inline.admin.NestedStackedInline):
    model = Litter
    extra = 0
    show_change_link = True
    inlines = [MouseInline]

class LitterAdmin(admin.ModelAdmin):
    list_display = ('breeding_cage', 'date_mated', 'age', 
        'date_toeclipped', 'date_weaned',
        'date_checked',  '_needs', 'need_date', 'notes',)
    inlines = [MouseInline] 
    list_editable = ('notes', 'date_weaned', 'date_checked')
    readonly_fields = ('_needs', 'need_date')

    def get_queryset(self, request):
        """Override the ordering to put future litters at the top"""
        qs = super(LitterAdmin, self).get_queryset(request)
        
        # Put the ones with no DOB first
        # Then the ones with no date of weaning
        # And for everyone else, sort in reverse chronological
        return qs.\
            annotate(dob_is_null=Count('dob')).\
            annotate(dwe_is_null=Count('date_weaned')).\
            order_by('dob_is_null', 'dwe_is_null', '-dob')
            
    ordering = ('proprietor',)

class CageAdmin(nested_inline.admin.NestedModelAdmin):
    list_display = ('name', 'proprietor', 'litter', 'infos', 'defunct', 'notes',)
    list_editable = ('notes', 'defunct', )
    ordering = ('defunct', 'proprietor', 'name',)
    readonly_fields = ('infos',)
    list_filter = ('proprietor',)
    inlines = [LitterInline]

class MouseAdmin(admin.ModelAdmin):
    #search_fields = ['name']
    
    # This controls the columns that show up on the Admin page for Mouse
    list_display = ('name', 'dob', 'age', 'sack_date', 'sex', 'cage', 
        'genotype', 'litter', 'notes')
    list_editable = ('sack_date', )
    readonly_fields = ('info', 'age', 'dob', 'mother', 'father')
    #~ list_display_links = ('name', 'litter', 'cage')
    list_filter = ['genotype', 'sack_date']
    
    # This controls what you see on the individual mouse page
    # Would be better to break this up into sections
    fieldsets = (
        (None, {
            'fields': ('name', 'dob', 'father', 'mother', 
            'manual_dob', 'manual_father', 'manual_mother',
            'age', 'sack_date', 'sex', 'cage', 'genotype', 'litter', 'notes', 'info'),
            'description': 'Specify manual_dob, manual_father, and manual_mother only if not available in litter info',
        }),
    )
    #ordering = ['dob']

class GenotypeAdmin(admin.ModelAdmin):
    ordering = ('name',)

class PersonAdmin(admin.ModelAdmin):
    ordering = ('name',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('assigned_to', 'created_by', 'notes', 'cage_names',)
    list_editable = ('notes',)

admin.site.register(Mouse, MouseAdmin)
admin.site.register(Genotype, GenotypeAdmin)
admin.site.register(Litter, LitterAdmin)
admin.site.register(Cage, CageAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Task, TaskAdmin)