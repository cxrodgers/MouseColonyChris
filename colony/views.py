from django.shortcuts import render
from django.views import generic

from .models import  Mouse, Cage

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'colony/index.html'
    model = Cage
    def get_queryset(self):
        return Cage.objects.order_by('defunct').all()

def cages(request):
    return render(request, 'colony/cages.html', {'cages': Cage.objects.all()})

#~ class MouseDetailView(generic.ListView):
    #~ model = Mouse
    #~ template_name = 'colony/mouse_detail.html'

#~ class CageDetailView(generic.ListView):
    #~ model = Cage
    #~ template_name = 'colony/cage_detail.html'