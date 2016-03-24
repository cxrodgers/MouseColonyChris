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

    
class BaseCage(models.Model):
    name = models.CharField(max_length=10)    
    status = models.CharField(max_length=100, blank=True, null=True)
    defunct = models.BooleanField(default=False)

    def n_mice(self):
        return len(self.mouse_set.all())
    
    def names(self):
        name_l = []
        for m in self.mouse_set.all():
            if m.training_name is not None and m.training_name != '':
                name_l.append(m.training_name)
            else:
                name_l.append(m.name)
        return ', '.join(name_l)
    
    def infos(self):
        info_l = [m.info() for m in self.mouse_set.all()]
        return '<pre>' + '<br>'.join(info_l) + '</pre>'
        #~ for m in self.mouse_set.all():
            #~ if m.training_name is not None and m.training_name != '':
                #~ info_l.append(m.training_name)
            #~ else:
                #~ info_l.append(m.name)
        #~ return ', '.join(info_l)        
    infos.allow_tags = True

    def age(self):
        age = None
        for mouse in self.mouse_set.all():
            if age is None:
                age = mouse.age()
            elif age != mouse.age():
                return None
        return age
    
    def __str__(self):
        return self.name

class BreedingCage(BaseCage):
    father = models.ForeignKey('Mouse',
        null=True, blank=True, related_name='bc_father',
        limit_choices_to={'sex': 0})
    mother = models.ForeignKey('Mouse',
        null=True, blank=True, related_name='bc_mother',
        limit_choices_to={'sex': 1})
    mother2 = models.ForeignKey('Mouse',
        null=True, blank=True, related_name='bc_mother2')
    purpose = models.CharField(max_length=50, blank=True, null=True)
    
    def target_genotype(self):
        res = ''
        if self.father is not None and self.father.genotype is not None:
            res += str(self.father.genotype)
        else:
            res += '?'
        
        res += ' x '
        
        if self.mother is not None and self.mother.genotype is not None:
            res += str(self.mother.genotype)
        else:
            res += '?'
        
        return res
    
    def litter_needs(self):
        for litter in self.litter_set.all():
            ln = litter._needs()
            if ln is not None:
                return ln
        return None

class BehaviorCage(BaseCage):
    location = models.IntegerField(
        choices=(
            (0, '1702'),
            (1, 'lab'),
            ),
        default=0,
        )

class Genotype(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Mouse(models.Model):
    name = models.CharField(max_length=10, unique=True)
    training_name = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField('date of birth', blank=True, null=True)
    tmx = models.CharField(max_length=50, blank=True, null=True)
    litter = models.ForeignKey('Litter', null=True, blank=True)
    sacked = models.BooleanField(default=False)
    headplate_color = models.CharField(max_length=15, blank=True, null=True)

    status = models.CharField(max_length=50, null=True, blank=True)

    # Could imagine derived classes TrainingMouse and BreederMouse
    # Mostly just so that TrainingMouse has a lot more task-specific info
    # But it's possible that BreederMouse become TrainingMouse
    # And there isn't any BreederMouse-specific info
    role = models.IntegerField(
        choices=(
            (0, 'waiting'),
            (1, 'training'),
            (2, 'vacation'),
            (3, 'breeder'),
            ),
        default=0,
        )
    
    sex = models.IntegerField(
        choices=(
            (0, 'M'),
            (1, 'F'),
            (2, '?'),
            )
        )
    
    # Link it to a cage
    cage = models.ForeignKey(BaseCage, null=True, blank=True)
    genotype = models.ForeignKey(Genotype)
    
    def auto_dob(self):
        """Auto dob
        
        Idea is that most of the time the dob doesn't have to specified bc
        we get it from the litter. So remove it from the inline.
        
        However in some cases we don't have litter, so allow user to specify
        manually in those cases.
        
        Then this is a read-only field to present the correct dob.
        """
        if self.manual_dob is not None:
            return self.manual_dob
        elif self.litter is not None:
            return self.litter.dob
        else:
            return None
    
    def info(self):
        """Returns TRAINING_NAME || NAME (SEX, AGE, GENOTYPE)
        
        """
        if self.training_name is not None and self.training_name != '':
            return self.training_name
        
        age = self.age()
        if age is None:
            return "%s (%s %s)" % (
                str(self.name),
                str(self.genotype),
                str(self.get_sex_display()),
                )
        else:
            return "%s (P%d %s %s)" % (
                str(self.name),
                self.age(),
                str(self.genotype),
                str(self.get_sex_display()),
                )
    
    def age(self):
        if self.dob is None:
            return None
        today = datetime.date.today()
        return (today - self.dob).days
    
    def __str__(self):
        if len(str(self.training_name)) > 0:
            return str(self.name) + '/' + str(self.training_name)
        else:
            return str(self.name)

class Litter(models.Model):
    name = models.CharField(max_length=20, unique=True)
    dpm = models.DateField('parents mated', null=True, blank=True)
    dob = models.DateField('date of birth', null=True, blank=True)
    dtc = models.DateField('toe clip', null=True, blank=True)
    dwe = models.DateField('weaned', null=True, blank=True)
    date_checked = models.DateField('last checked', null=True, blank=True)
    
    # This should really be called breeding_cage
    cage = models.ForeignKey(BreedingCage, null=True)
    
    # These should be determined from breeding_cage
    #~ father = models.ForeignKey(Mouse, null=True, blank=True, related_name='litter_father')
    #~ mother = models.ForeignKey(Mouse, null=True, blank=True, related_name='litter_mother')
    status = models.CharField(max_length=50, null=True, blank=True)
    pcr_info = models.CharField(max_length=50, null=True, blank=True)
    needs = models.CharField(max_length=50, null=True, blank=True)
    need_date = models.DateField('needs on', null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    def _needs(self):
        """View column in admin that triggers update_needs
        
        When the admin requests this, it calls update_needs, which sets
        needs and need_date. This returns needs.
        
        Seems like there is a slight race condition in that need_date might
        be requested before needs, which means it would be stale. But
        refreshing would fix this..
        """
        self.update_needs()
        return self.needs
        
    def update_needs(self):
        """Automatically determine next needed action and date.
        
        Sets the fields "needs" and "need_date".
        """
        if self.dwe is not None:
            # Already weaned
            self.needs = None
            self.need_date = None
        elif self.dtc is not None:
            # Already toe clipped, needs wean
            if self.dob is None:
                self.needs = "provide dob"
                self.need_date = datetime.date.today()
                return
            self.need_date = self.dob + datetime.timedelta(days=19)
            self.needs = "wean on P19"
        elif self.dob is not None:
            # Born, but not toe clipped
            self.need_date = self.dob + datetime.timedelta(days=7)
            self.needs = "toe clip on P7"
        elif self.dpm is not None:
            # Not born yet
            self.need_date = self.dpm + datetime.timedelta(days=25)
            
            # If it was checked since the target date, extend by 4 days
            if self.date_checked is not None and self.date_checked > self.need_date:
                self.need_date = self.date_checked + datetime.timedelta(days=4)
            
            # Recalculate the time taken
            gestation_period = (self.need_date - self.dpm).days
            self.needs = "check for pups on day %d" % gestation_period
        else:
            # Not even mated
            self.needs = "parent"
            self.need_date = datetime.date.today()
    
    

class Desideratum(models.Model):
    description = models.CharField(max_length=150, null=True, blank=True)
    mice = models.ManyToManyField(Mouse, blank=True)
    