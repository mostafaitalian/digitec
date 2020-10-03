from django.db import models
from customer.models import Customer, Department
from engineer.models import Area, Engineer
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.transaction import atomic
# Create your models here.
#print(datetime.now()+datetime)
def get_upload_name(instance, filename):
    if hasattr(instance, 'review_title'):
        return u'{}/{}/{}_{}'.format(instance.engineer.name, instance.review_title, instance.review_title, filename)
    elif hasattr(instance, 'review'):
        return u'{}/{}/{}_{}'.format(instance.review.engineer.name, instance.review.review_title, instance.review.review_title, filename)

    else:
        return filename
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
    def get_machines_by_customer(self,customer_id=None):
        if customer_id:
            return Machine.objects.filter(customer__id=customer_id)
        else:
            return None 
class Machine(MachineDetail):
    bw_workcentre = 'mono workcentre'
    color_workcentre = 'color workcentre'
    bw_phasor = 'mono phasor'
    color_phasor = 'color phasor'
    wide_format = 'wide format'

    category_choices = ((bw_workcentre,'B/W workcentre'),(color_workcentre,'Color workcentre'), (bw_phasor,'B/W phasor'),
    (color_phasor,'Color phasor'), (wide_format,'Wide Format'))
    
    # category = models.ForeignKey(Category, on_delete=models.CASCADE,  blank=True, null=True)
    machine_category = models.CharField('Machine Category',max_length=100,choices=category_choices, blank=True,null=True)
    customer = models.ForeignKey(Customer,related_name='machines', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='machines_dep', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, related_name='machines', on_delete=models.CASCADE, blank=True,null=True)
    engineers = models.ManyToManyField(Engineer, related_name='machines', blank=True)
    contract = models.ForeignKey(to='Contract', on_delete=models.CASCADE,related_name='machines', null=True, blank=True)
    #call = models.OneToOneField()
    objects = models.Manager()
    objects1 = MachineManager()
    def __str__(self):
        return self.machine_model + '({})'.format(self.machine_category)+"  "+self.customer.name+"  "+self.department.department_name
    # def save(self,*args,**kwargs):
    #     department = Department.objects.get(pk=self.department.id)
    #     department.no_of_machine +=1

    #     department.save(update_fields=['no_of_machine'])
    #     self.department = department
    #     super().save(*args,**kwargs)
class Call(models.Model):
    #from machine.models import Machine
    unassigned = 'unassigned'
    pending = 'pending'
    completed =  'completed'
    dispatched =  'dispatched'
    status_choices = ((unassigned, 'Unassigned'),(dispatched, 'Dispatched'), (pending, 'Pending'),(completed, 'Completed'))
    def customer_name(self):
        machine = Machine.objects.get(id=self.machine.id)
        customer = Customer.objects.get(id=machine.customer.id)
        return customer.name
    notification_number = models.AutoField(primary_key=True, blank=True)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer,related_name='calls',on_delete=models.CASCADE, blank=True, null=True)
    machine = models.ForeignKey(to='Machine', related_name='calls', on_delete=models.CASCADE)
    is_assigned = models.BooleanField("indicate wheather call has engineer or not", default=False)
    status = models.CharField('Status', max_length=20 , choices=status_choices, default=unassigned)
    previous_status = models.CharField(max_length=50,help_text='do not fill this anywhere', null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    response_time_end_date= models.DateTimeField(null=True,blank=True)    
    assigned_date = models.DateTimeField(blank=True, null=True)
    optimum_completed_date = models.DateTimeField(help_text="the default value is 6 hours + assign_date", null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    def getResponseTime(self):
        customer_start_time  =  self.customer.begin_at
        customer_finish_time = self.customer.finish_at
        engineer_start_time = datetime.time(hour=8)
        engineer_finish_time = datetime.time(hour=16)
        response_margin = 6
        call_create_date = self.created_date
        
    #     pass



    class Meta:
        get_latest_by=['notification_number']
   
    def __str__(self):
        if self.engineer:
                return (Engineer.objects.get(id=self.engineer.id).name) + ' ' + self.customer.name + ' ' + self.machine.name + ' ' +str(self.notification_number)
        return self.machine.name + ' ' + self.customer.name + ' ' + str(self.notification_number) + ' ' + ' no engineer assigned yet'
    # def save(self, *args, **kwargs):
    #     if self.engineer:
    #         self.is_assigned = True
    #         # self.status = 'pending'
    #         # self.engineer.no_of_calls += 1
    #         self.engineer.save()
    #         # self.engineer.no_of_calls_pending = 0
    #         # self.engineer.no_ofcalls_success = 0
    #     else:

    #         self.is_assigned=False
        
    #     super().save(*args, **kwargs)



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

class Report(models.Model):
    # def get_customer(self):
    #     return self.call.machine.customer.name
    pending = 'pending'
    completed =  'completed'
    status_choices = ((pending, 'Pending'),(completed, 'Completed'))

    call = models.ForeignKey(Call, related_name='reports', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=50,default='')
    engineer = models.ForeignKey(Engineer,related_name='calls', on_delete=models.CASCADE)
    notification_number = models.IntegerField(null=True, blank=True)
    machine_serial = models.IntegerField(blank=True, null=True)
    billing_meter_black = models.IntegerField(blank=True, null=True)
    billing_meter_color = models.IntegerField(blank=True, null=True)

    billing_meter_total = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=status_choices, default=pending)
    billing_meter1 = models.IntegerField(blank=True, null=True)
    billing_meter2 = models.IntegerField(blank=True, null=True)
    report_copy = models.FileField(upload_to='files/reports/', blank=True, null=True)
    image = models.ImageField(upload_to='images/reports/', blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    notes_for_dispatcher = models.TextField(blank=True, null=True)
    # def save(self, *args, **kwargs):
    #     self.call.status=self.status
    #     self.call.save()
        # self.save()
        # if self.status == 'pending':
        #     call = Call.objects.get(notification_number=self.call.notification_number)
        #     call.status='pending'
        #     print(call.notification_number)
        #     print(call.status)
            
        #     call.save()
        #     self.call = call
            # self.call.status='pending'
            # self.call.save()
            # self.save()
        # elif self.status=='completed':
        #     call = Call.objects.get(notification_number=self.call.notification_number)
        #     call.status='completed'
        #     call.save()
        #     self.call = call
            
            # self.call.status='completed'
            # self.call.save()
            # self.save()

        # super().save(*args,**kwargs)
    def __str__(self):
        return str(self.call.notification_number) + ' ' + self.engineer.name + ' ' +self.call.status

class Contract(models.Model):
    fsma='FSMA'
    xpps='XPPS'
    labour='Time'
    fm='FM'
    lis = 'LIS'
    contract_choices=((fsma, 'FSMA'), (labour, 'Time'), (lis,'LIS'),(fm, 'FM'), (xpps,'XPPS'))
    
    contract_type = models.CharField(max_length=50,choices=contract_choices, blank=True, null=True)
    def __str__(self):
        return self.contract_type

class EngineerReview(models.Model):
    engineer = models.ForeignKey(Engineer, related_name='reviews', on_delete=models.CASCADE)
    machine= models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    review_title = models.CharField(max_length=200)
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank='True')
    state_choices = (('pending','pending'),('published','published'),('rejected','rejected'))
    status=models.CharField(max_length=50, choices=state_choices)
    file_data = models.FileField(upload_to=get_upload_name, blank=True, null=True)
    image = models.ImageField(upload_to=get_upload_name, blank=True, null=True)    
    
    class Meta:
        permissions=(('can_approve_or_reject_review','can approve or reject review'),)
        
    def __str__(self):
        return self.engineer.name + ' - ' + self.review_title
class Comment(models.Model):
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    engineer_review = models.ForeignKey(EngineerReview, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text

class ImageAbstract(models.Model):

    image_name = models.CharField('Image name',max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to=get_upload_name, blank=True, null=True)
    image_description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class FileAbstract(models.Model):
    file_name = models.CharField('Image name',max_length=50, blank=True, null=True)
    file1 = models.ImageField(upload_to='images/', blank=True, null=True)
    file_description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class ImageReview(ImageAbstract):

    review = models.ForeignKey(EngineerReview, related_name='images', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.image_name + ' ' + self.review.machine.name + ' ' +self.review.review_title


class FileReview(models.Model):
    review = models.ForeignKey(EngineerReview, related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name + ' ' + self.review.machine.name + ' ' +self.review.review_title


class ImageReport(ImageAbstract):
    report = models.ForeignKey(Report, related_name='images', on_delete=models.CASCADE)


    def __str__(self):
        return self.image_name + ' ' + self.report.call.notification_number


class FileReport(FileAbstract):
    Report = models.ForeignKey(Report, related_name='files', on_delete=models.CASCADE)


    def __str__(self):
        return self.file_name + ' ' + self.report.call.notification_number