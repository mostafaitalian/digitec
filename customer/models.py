from django.db import models
from django.urls.base import reverse_lazy
from engineer.models import Engineer
from engineer.models import Area
import random
import datetime
from _datetime import timedelta
#from machine.models import Machine
# Create your models here.
def get_machine_number(instance):
    total_number = 0
    if instance.customers:
        for customer in instance.customers:
            if customer.departments:
                total_number = sum([d.no_of_machines for d in customer.departments.all()])
        return total_number
    else:
        return 0

class CustomerDetail(models.Model):
    name = models.CharField(unique=True, max_length=100)
    # slug = models.SlugField(help_text='donot fill this it will be filled automatically',unique=True, blank=True)
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
    Saturday = 0
    Sunday = 1
    Monday = 2
    Tuesday = 3
    Wednesday = 4
    Thursday = 5
    Friday = 6
    NoDayoff = 7
    weekday_choices = ((Saturday, 'Saturday'),(Sunday, 'Sunday'),(Monday, 'Monday'),(Tuesday, 'Tuesday'),(Wednesday, 'Wednesday'),(Thursday, 'Thursday'),(Friday, 'Friday'),(NoDayoff, 'NoDayoff'))


    #departments = models.ManyToManyField(to=Department, related_name='customer')
    location = models.CharField('Address location',max_length=255)
    address = models.URLField('address site')
    telephone = models.PositiveIntegerField("telephone", null=True, blank=True)
    #machines = models.ForeignKey(Machine, on_delete=models.CASCADE)
    area = models.ForeignKey(to=Area, related_name='customers',to_field='slug', on_delete=models.CASCADE)
    engineers = models.ManyToManyField(to=Engineer, related_name='customers', blank=True)
    begin_at = models.TimeField(default=datetime.time(hour=8, minute=0, second=0))
    finish_at = models.TimeField(default=datetime.time(hour=16, minute=0, second=0))
    organization = models.ForeignKey(to='CustomerOrganization',on_delete=models.CASCADE, related_name='customers',null=True, blank=True)
    first_week_dayoff = models.IntegerField(choices=weekday_choices, default=7)
    second_week_dayoff = models.IntegerField(choices=weekday_choices, default=7)
    


    def save(self, *args, **kwargs):
        self.slug = self.name + '_' + str(random.randint(a=1,b=9999999))
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse_lazy('customer:customer-detail', id=self.id)
    
    def get_machine_number(self):
        if self.machines:
            return self.machines.all().count()
        else:
            return 0
    
    def __str__(self):
        return self.name

class CustomerBranch(CustomerDetail):
    def get_machine_number(self):
        if self.machines:
            return self.machines.all().count()
        else:
            return 0

    #departments = models.ManyToManyField(to=Department, related_name='customer')
    location = models.CharField('Address location',max_length=255)
    address = models.URLField('address site')
    telephone = models.PositiveIntegerField("telephone", null=True, blank=True)
    #machines = models.ForeignKey(Machine, on_delete=models.CASCADE)
    # area = models.ForeignKey(to=Area, related_name='customers',to_field='slug', on_delete=models.CASCADE)
    # engineers = models.ManyToManyField(to=Engineer, related_name='customer_branches', blank=True)
    begin_at = models.TimeField(default=datetime.time(hour=8, minute=0, second=0))
    finish_at = models.TimeField(default=datetime.time(hour=16, minute=0, second=0))
    organization = models.ForeignKey(to='CustomerOrganization',on_delete=models.CASCADE, related_name='branches')
    # branche_machines_number = models.PositiveIntegerField(default=get_machine_number)


    # def save(self, *args, **kwargs):
    #     self.slug = self.name + '_' + str(random.randint(a=1,b=9999999))
    #     super().save(*args, **kwargs)
    
    # def get_absolute_url(self):
    #     return reverse_lazy('customer:customer-detail', id=self.id)
    

    
    def __str__(self):
        return self.name
class CustomerOrganization(CustomerDetail):


    name= models.CharField(max_length=50)
    discription = models.TextField(null=True,blank=True)
    organization_machines_number = models.PositiveIntegerField(default=0)
    #departments = models.ManyToManyField(to=Department, related_name='customer')
    # location = models.CharField('Address location',max_length=255)
    # address = models.URLField('address site')
    # telephone = models.PositiveIntegerField("telephone", null=True, blank=True)
    # machines = models.ForeignKey(Machine, on_delete=models.CASCADE)
    # area = models.ForeignKey(to=Area, related_name='customers',to_field='slug', on_delete=models.CASCADE)
    # engineers = models.ManyToManyField(to=Engineer, related_name='customers', blank=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        
        total_number = 0
        if self.customers:
            for customer in self.customers.all():
                if customer.departments:
                    total_number += sum([d.no_of_machine for d in customer.departments.all()])
            self.organization_machines_number = total_number
            # self.save(update_fields=['organization_machines_number'])
        else:
            self.organization_machines_number = 0
            # self.save(update_fields=['organization_machines_number'])

        super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     self.slug = self.name + '_' + str(random.randint(a=1,b=9999999))
    #     super().save(*args, **kwargs)
    
    # def get_absolute_url(self):
    #     return reverse_lazy('customer:customer-detail', id=self.id)
    


    def __str__(self):
        return self.name

class ContactPerson(models.Model):
    first_name=models.CharField('First Name', max_length=20)
    last_name=models.CharField('Last Name', max_length=20)
    email = models.EmailField()
    mobile_number = models.PositiveIntegerField('Mobile Number',null=True,blank=True)
    office_number = models.PositiveIntegerField('Office Number',null=True,blank=True)
    cutomer = models.ForeignKey(CustomerBranch, on_delete=models.CASCADE, related_name='contact_persons')



    def __str__(self):
        if self.customer:
            return self.name + "(" + self.customer.name +")"
        else:
            return self.name