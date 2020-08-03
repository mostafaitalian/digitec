from django.db import models
from django.urls.base import reverse_lazy
from engineer.models import Engineer
from engineer.models import Area
#from machine.models import Machine
# Create your models here.


class CustomerDetail(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    class Meta:
        abstract=True

class Department(models.Model):
    section=(('HR section', 'HR'),
             ('Service section','Service'),
             ('Finance section','Finance'),
             ('Collection section','Collection'),
             ('Sales section','Sales'),
             ('Production section','Production'),
             ('others','others'))
    department_name = models.CharField(choices=section,max_length=200,blank=True)
    no_of_machine = models.PositiveIntegerField('machines number', default=0)
    customer = models.ForeignKey(to='Customer', related_name='departments', on_delete=models.CASCADE )
    def __str__(self):
        return self.department_name + "  " + self.customer.name
class Customer(CustomerDetail):
    #departments = models.ManyToManyField(to=Department, related_name='customer')
    location = models.CharField('Address location',max_length=255)
    address = models.URLField('address site')
    telephone = models.PositiveIntegerField("telephone", null=True, blank=True)
    #machines = models.ForeignKey(Machine, on_delete=models.CASCADE)
    area = models.ForeignKey(to=Area, related_name='customers',to_field='slug', on_delete=models.CASCADE)
    engineers = models.ManyToManyField(to=Engineer, related_name='customers', blank=True)
    
    
    def get_absolute_url(self):
        return reverse_lazy('customer:detail', slug=self.slug)
    
    def get_machine_number(self):
        if self.machine_set:
            return self.machine_set.all().count()
        else:
            return self.machine_set.all().count()
    
    def __str__(self):
        return self.name