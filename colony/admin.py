from django.contrib import admin
from .models import (Mouse, Genotype, Litter, 
    BreedingCage, BaseCage, BehaviorCage, Desideratum)
# Register your models here.
from django.db.models import Count


class MouseInline(admin.TabularInline):
    model = Mouse
    extra = 1
    show_change_link = True    

class LitterInline(admin.TabularInline):
    model = Litter
    extra = 1
    show_change_link = True

class LitterAdmin(admin.ModelAdmin):
    list_display = ('name', 'cage', 'dpm', 'dob', 'dtc', 'dwe',
        'date_checked', 'status', '_needs', 'need_date')
    inlines = [MouseInline] 
    list_editable = ('status', 'dwe', 'date_checked')
    readonly_fields = ('_needs', 'need_date')

    def get_queryset(self, request):
        """Override the ordering to put future litters at the top"""
        qs = super(LitterAdmin, self).get_queryset(request)
        
        # Put the ones with no DOB first
        # Then the ones with no date of weaning
        # And for everyone else, sort in reverse chronological
        return qs.\
            annotate(dob_is_null=Count('dob')).\
            annotate(dwe_is_null=Count('dwe')).\
            order_by('dob_is_null', 'dwe_is_null', '-dob')


class BreedingCageAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'n_mice', 'age', 'infos', 'defunct', 'purpose', 
        'target_genotype', 'status', 'father', 'mother', 'litter_needs')
    list_editable = ('defunct', 'purpose', 'status')
    #~ list_display_links = ('father', 'mother',)
    readonly_fields = ('n_mice', 'names', 'target_genotype', 'infos', 'litter_needs')
    ordering = ('defunct', 'name',)
    inlines = [MouseInline, LitterInline]
    
class BehaviorCageAdmin(admin.ModelAdmin):
    list_display = ('name', 'n_mice', 'age', 'infos', 'location', 'status')    
    readonly_fields = ('n_mice', 'names', 'infos', 'age',)
    list_editable = ('location', 'status',)
    ordering = ('name',)
    inlines = [MouseInline]

class MouseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'training_name', 'age', 'sacked', 'sackDate', 'sex', 'dob', 'cage', 
        'genotype', 'role', 'litter', 'status')
    list_editable = ('sacked', )
    readonly_fields = ('info', 'age',)
    #~ list_display_links = ('name', 'litter', 'cage')
    list_filter = ['role', 'genotype', 'sacked']
    ordering = ['dob']

class GenotypeAdmin(admin.ModelAdmin):
    ordering = ('name',)

class DesideratumAdmin(admin.ModelAdmin):
    list_display = ('description', )#, 'mice')

admin.site.register(Mouse, MouseAdmin)
admin.site.register(BreedingCage, BreedingCageAdmin)
admin.site.register(BehaviorCage, BehaviorCageAdmin)
admin.site.register(Genotype, GenotypeAdmin)
admin.site.register(Litter, LitterAdmin)
admin.site.register(BaseCage)
admin.site.register(Desideratum, DesideratumAdmin)