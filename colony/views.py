from django.shortcuts import render
from django.views import generic

from .models import ChrisMouse, ChrisCage

# Create your views here.

class IndexView(generic.ListView):
    """Returns all cages sorted by name for the CensusView to display"""
    template_name = 'colony/index.html'
    model = ChrisCage
    def get_queryset(self):
        return ChrisCage.objects.order_by('name').all()

def cages(request):
    """Return view of cages for django_tables2
    
    This has basically been replaced by the IndexView above.
    """
    return render(request, 'colony/cages.html', 
        {'cages': ChrisCage.objects.order_by('-name').all()})
