from django.db import models
# from machine.models import Machine
from django.conf import settings
from django.utils import timezone
#from machine.models import Machine
# Create your models here.
class Area(models.Model):
    name= models.CharField('area code',max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    margin = models.URLField()
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.name+self.start+self.end
        #self.save()
        super().save(*args,**kwargs)
class Engineer(models.Model):
    name=models.CharField('xerox username',max_length=255, help_text="start with 'EGD20' and followed by your number")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    joining_date = models.DateField()
    no_of_calls = models.PositiveIntegerField(default=0)
    no_of_calls_pending = models.PositiveIntegerField(default=0)
    no_of_calls_dispatched = models.PositiveIntegerField(default=0)

    no_ofcalls_success = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
        

        