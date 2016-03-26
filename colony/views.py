from django.shortcuts import render
from django.views import generic

from .models import  Mouse, BaseCage, BreedingCage, BehaviorCage

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'colony/index.html'
    model = BreedingCage
    def get_queryset(self):
        return BreedingCage.objects.order_by('defunct').all()

#~ class MouseDetailView(generic.ListView):
    #~ model = Mouse
    #~ template_name = 'colony/mouse_detail.html'

#~ class CageDetailView(generic.ListView):
    #~ model = Cage
    #~ template_name = 'colony/cage_detail.html'