"""
TODO
Validation scripts that check that the genotype of each mouse meshes with
the parents
Auto-determine needed action for each litter (and breeding cage?)
Auto-id litters
Slug the mouse name from the litter name and toe num?
"""


from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.

class ChrisCage(models.Model):
    name = models.CharField(max_length=10, unique=True)    
    
    def __str__(self):
        return self.name

class ChrisGenotype(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class ChrisMouse(models.Model):
    # Required fields
    name = models.CharField(max_length=15, unique=True)
    sex = models.IntegerField(
        choices=(
            (0, 'M'),
            (1, 'F'),
            (2, '?'),
            )
        )
    genotype = models.ForeignKey(ChrisGenotype)
    
    # Optional fields that can be set by the user
    cage = models.ForeignKey(ChrisCage, null=True, blank=True)
    
    # Chris-specific optional fields
    training_name = models.CharField(max_length=20, null=True, blank=True)
    headplate_color = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name