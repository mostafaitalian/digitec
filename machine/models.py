from django.db import models
from customer.models import Customer, Department
from engineer.models import Area, Engineer
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
# Create your models here.
#print(datetime.now()+datetime)

User = get_user_model()
def get_upload_name(instance, filename):
    if hasattr(instance, 'review_title'):
        return u'{}/{}/{}_{}'.format(instance.engineer.name, instance.review_title, instance.review_title, filename)
    elif hasattr(instance, 'review'):
        return u'{}/{}/{}_{}'.format(instance.review.engineer.name, instance.review.review_title, instance.review.review_title, filename)

    else:
        return filename
speed_choices=((10,10), (15,15), (20,20),(25,25),(30,30),(35,35),(45,45),(55,55),(65,65),(75,75),(90,90))
class MachineDetail(models.Model):
    model_choices = (('5855', '5855'), ('5845', '5845'), ('5955', '5955'), ('5945', '5945'),
    ('5865', '5865'), ('5875', '5875'), ('7830', '7830'), ('7845', '7845'), ('7855', '7855'),
    ('7835', '7835'), ('7225', '7225'), ('7120', '7120'),
    ('c60', 'c60'), ('c70', 'c70'),
    ('560', '560'), ('550', '550'),
    ('j60', 'j60'),
    ('b7025', 'b7025'), ('b7030', 'b7030'), ('b7035', 'b7035'),
    ('5325', '5325'), ('5330', '5330'), ('5335', '5335'),
    ('5016', '5016'), ('5020', '5020'),
    ('5019', '5019'), ('5021', '5021'),
    ('5022', '5022'), ('5024', '5024'),
    ('5735', '5735'), ('5745', '5745'), ('5755', '5755'), ('5765', '5765'), ('5790', '5790'),
    ('5635', '5635'), ('5645', '5645'), ('5655', '5655'), ('5665', '5665'), ('5690', '5690'),
    ('3655', '3655'),
    ('3635', '3635'),
    ('3615', '3615'),
    ('8880', '8880'), ('8870', '8870'),
    ('5225', '5225'), ('5230', '5230'), ('5235', '5235'), ('5225A', '5225A'), ('5230A', '5230A'), ('5235A', '5235A'),
    ('4150', '4150'), ('4260', '4260'),
    ('b405', 'b405'), ('c405', 'c405'),
    ('c7025', 'c7025'), ('c7030', 'c7030'), ('c7035', 'c7035'),
    ('b8045', 'b8045'), ('b8055', 'b8055'),
    ('c8035', 'c8035'), ('c8045', 'c8045'), ('c8055', 'c8055'), ('c8065', 'c8065'), ('c8075', 'c8075'),
    ('180', '180'), ('2100', '2100'), ('3100', '3100'))
    production  = 4
    workcentre = 6
    radiology = 6
    phasor = 9
    production_return = 4
    production_return_meter = 2000
    office_return = 7
    office_return_meter = 5000
    radiology_return = 7
    radiology_return_meter = 5000

    response_choices_hours = ((production, 'Production'),(workcentre, 'Workcentre'), (phasor, 'Phasor'),(radiology, 'Radiology'))
    return_choices_days = ((production_return, 'Production'), (office_return, 'Office'), (radiology_return, 'Radiology'))
    serial = models.IntegerField('standard seial', help_text='fill this if your serial is numbers only', unique=True, blank=True)
    serial2 = models.CharField('non-standard serial', max_length=10, help_text="fill this if your serial consists of numbers and letters", unique=True, blank=True)
    machine_model = models.CharField(max_length=100)
    model_of_machine =models.CharField('model of machine',max_length=10, choices=model_choices, default='no model')
    slug = models.SlugField(unique=True)
    description = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    speed = models.IntegerField(blank = True, null=True, choices=speed_choices)
    machine_points = models.FloatField(default=1)
    machine_response_time = models.IntegerField(choices=response_choices_hours, null=True, blank=True)
    machine_return_time = models.IntegerField(choices=return_choices_days, null=True, blank=True) 
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
    contract = models.OneToOneField(to='Contract', on_delete=models.DO_NOTHING, related_name='machine', null=True, blank=True)
    #call = models.OneToOneField()
    objects = models.Manager()
    objects1 = MachineManager()
    def __str__(self):
        return '{}'.format(self.serial) + ' ' +self.machine_model + '({})'.format(self.machine_category)+"  "+self.customer.name+"  "+self.department.department_name
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
    previous_engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True, blank=True, related_name='previous_engineer_calls')
    fault = models.TextField(null=True, blank=True)
    notes_from_customer = models.TextField(null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    response_time_end_date= models.DateTimeField(null=True,blank=True)    
    assigned_date = models.DateTimeField(blank=True, null=True)
    optimum_completed_date = models.DateTimeField(help_text="the default value is 6 hours + assign_date", null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    real_assigned_date=models.DateTimeField(null=True, blank=True)
    real_completed_date = models.DateTimeField(null=True, blank=True)
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
    tandm = 'T&M'
    contract_choices=((fsma, 'FSMA'), (labour, 'Time'), (lis,'LIS'),(fm, 'FM'), (xpps,'XPPS'), (tandm, 'T&M'))
    
    contract_type = models.CharField(max_length=50,choices=contract_choices, blank=True, null=True)
    machine_serial = models.IntegerField(null=True,  blank=True)
    monthly_fees = models.DecimalField('monthly fees', max_digits=5, decimal_places=2, null=True, blank=True)
    
    start_of_contract = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    end_of_contract = models.DateTimeField(help_text="do not fill this field it will add a year automatically", null=True, blank=True)
    # def save(self, *args, **kwargs):
    #     if self.contract_type == 'T&M':
    #         self.monthly_fees = 0.0
    #     if self.start_of_contract is None:
    #         self.start_of_contract = datetime.now()
    #     if self.start_of_contract:
    #         self.end_of_contarct=self.start_of_contract + relativedelta(years=1)
                        # if instance.machine
        # try:
        #     uu= kwargs.pop('update_fields')
        #     print(uu)
        #     if self.machine.exist():
        #         print('h1')
        #         self.machine_serial = 3
        #         self.save()

        # except:
        #     self.machine_serial =2
        #     print('h2')
        #     # instance.save()

        # super().save(*args, **kwargs)
                    

    def __str__(self):
        return self.contract_type + " " + '{}'.format(self.monthly_fees)
    



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

class Contact(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contact', null=True, blank=True)
    first_name = models.CharField('First name', max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    mobile = models.IntegerField()
    telephone = models.PositiveIntegerField(null=True, blank=True)
    email_address = models.EmailField(null=True,blank=True)
    call = models.ForeignKey(Call, on_delete=models.DO_NOTHING, related_name='call_contacts')





    def __str__(self):
        # if self.user is None:
        #     return self.first_name + " " +self.last_name
        # else:
        #     return self.first_name + " " +self.last_name + " " + self.user.username
        return self.first_name+ ''+self.last_name



