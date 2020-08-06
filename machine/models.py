from django.db import models
from customer.models import Customer, Department
from engineer.models import Area, Engineer
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.transaction import atomic
# Create your models here.
#print(datetime.now()+datetime)
speed_choices=((20,20),(30,30),(35,35),(45,45),(55,55),(65,65),(75,75),(90,90))
class MachineDetail(models.Model):
    name= models.CharField(max_length=200)
    serial = models.IntegerField('standard seial', help_text='fill this if your serial is numbers only', unique=True, blank=True)
    serial2 = models.CharField('non-standard serial', max_length=10, help_text="fill this if your serial consists of numbers and letters", unique=True, blank=True)
    machine_model = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    speed = models.IntegerField(blank = True, null=True, choices=speed_choices)
    
    class Meta:
        abstract=True
class Category(models.Model):
    type_choice= (('black-white machine','B&W Machine'),('color machine', 'Colour Machine'),('White Format machine','White-Format machine'))
    category_type = models.CharField(max_length=150, choices=type_choice, unique=True)
    def __str__(self):
        return self.category_type

class MachineManager(models.Manager):
    def get_machines_by_customer(self,customer=None):
        if customer:
            return Machine.objects.filter(customer=customer)
        else:
            return None 
class Machine(MachineDetail):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,related_name='machines', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='machines_dep', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, related_name='machines', on_delete=models.CASCADE, blank=True,null=True)
    engineers = models.ManyToManyField(Engineer, related_name='machines', blank=True)
    #call = models.OneToOneField()
    objects = MachineManager()
    def __str__(self):
        return self.machine_model + '({})'.format(self.category)+"  "+self.customer.name+"  "+self.department.department_name
    def save(self,*args,**kwargs):
    
        self.department.no_of_machine +=1
        self.department.save()
        super().save(*args,**kwargs)
class Call(models.Model):
    #from machine.models import Machine
    assigned = 'assigned'
    unassigned = 'unassigned'
    pending = 'pending'
    completed =  'completed'
    status_choices = ((assigned, 'Assigned'), (unassigned, 'Unassigned'), (pending, 'Pending'),(completed, 'Completed'))
    def customer_name(self):
        machine = Machine.objects.get(id=self.machine.id)
        customer = Customer.objects.get(id=machine.customer.id)
        return customer.name
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer,related_name='calls',on_delete=models.CASCADE, blank=True, null=True)
    machine = models.ForeignKey(to='Machine', related_name='calls', on_delete=models.CASCADE)
    assign_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(help_text="the default value is 6 hours + assign_date", default=datetime.now()+timedelta(hours=6))
    notification_number = models.AutoField(primary_key=True, blank=True)
    is_assigned = models.BooleanField("indicate wheather call has engineer or not", default=False)
    status = models.CharField('Status', max_length=20 , choices=status_choices, default=unassigned)

    class Meta:
        get_latest_by=['notification_number']
   
    def __str__(self):
        if self.engineer:
                return (Engineer.objects.get(id=self.engineer.id).name)
        return self.machine.name + ' no engineer assigned yet'
    def save(self, *args, **kwargs):
        if self.engineer:
            self.is_assigned = True
            self.status = 'assigned'
            self.engineer.no_of_calls += 1
            self.engineer.save()
            # self.engineer.no_of_calls_pending = 0
            # self.engineer.no_ofcalls_success = 0
            
        super().save(*args, **kwargs)




























    
'''class ex(models.Field):
    def db_type(self, connection):
        if connection.setting_dict['ENGINE']=='django.db.backends.mysql':
            return 'datetime'
        else:
            return 'timestamp

    def get_end_date(self):
        #d = datetime.now()
        d= self.assign_date
        if d.hour+6 >= 24:
    
            t = datetime(d.year, d.month, d.day+1, d.hour+6-24)
            print(t)
            return t
        else:
            t = datetime(d.year, d.month, d.day+1, d.hour+6)
            return t
 def save(self,*args,**kwargs):
        with atomic():
            #last_notification = Call.objects.latest('id').select_for_update(nowait=False).notification_number
            if Call.objects.all():
                
                self.notification_number = Call.objects.all().count()+1
                self.save()
                #self.notification_number += 1
            else:
                self.notification_number=1
                self.save()
 def save(self,*args,**kwargs):
        with atomic():
            #last_notification = Call.objects.latest('id').select_for_update(nowait=False).notification_number
            if Call.objects.all():
                
                self.notification_number = Call.objects.all().count()+1
                self.save()
                #self.notification_number += 1
            else:
                self.notification_number=1
                self.save()'''