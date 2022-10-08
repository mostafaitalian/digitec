from django.db import models
from customer.models import Customer, Department
from engineer.models import Area, Engineer
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
import datetime
# Create your models here.
#print(datetime.now()+datetime)

User = get_user_model()
def get_upload_name(instance, filename):
    if hasattr(instance, 'review_title'):
        return u'{}/{}/{}_{}'.format(instance.engineer.name, instance.review_title, instance.review_title, filename)
    elif hasattr(instance, 'review'):
        return u'{}/{}/{}_{}'.format(instance.review.engineer.name, instance.review.review_title, instance.review.review_title, filename)
    elif hasattr(instance, 'report'):
        return u'{}/{}/{}_{}'.format(instance.report.engineer.name, instance.report.call.notification_number, instance.report.id, filename)

    else:
        return filename
speed_choices=((10,10), (15,15), (20,20),(25,25),(30,30),(35,35),(45,45),(55,55),(65,65),(75,75),(90,90))
class MachineDetail(models.Model):
    #machine model choices
    model_choices = (('5855', '5855'), ('5845', '5845'), ('5955', '5955'), ('5945', '5945'),
    ('5865', '5865'),('5875', '5875'), ('5890', '5890'),
    ('6510', '6510'), ('6515', '6515'),
    ('7428','7428'),

    ('7530','7530'),('7535','7535'),('7545','7545'),('7555','7555'),('7565','7565'),
    ('7830', '7830'), ('7845', '7845'), ('7855', '7855'),
    ('7835', '7835'),
    ('7220','7220'), ('7225', '7225'), ('7120', '7120'), ('7125', '7125'), ('7132','7132'),('7232', '7232'),('7242','7242'),
    ('7221', '7221'), ('7121', '7121'),
    ('7328', '7328'),('7365', '7365'), ('7366', '7366'),
    ('6655', '6655'), ('6645','6645'),
    ('pe220', 'pe220'), ('PE220', 'PE220'), ('PE16', 'PE16'), ('pe16', 'pe16'),
    ('pe120', 'pe120'), ('PE120', 'PE120'),
    ('b1022', 'b1022'), ('b1025', 'b1025'), ('1022B', '1022B'),
    ('1025B', '1025B'),('1025', '1025'), ('1022', '1022'),
    ('B215', 'B215'), ('b215', 'b215'), ('215B', '215B'), ('215b', '215b'),
    ('b605', 'b605'), ('b615', 'b615'), ('605B', '605B'), ('615B', '615B'),
    ('B605', 'B605'),('B615','B615'), ('605b', '605b'), ('615b', '615b'),
    ('510', '510'),


    ('c9065', 'c9065'), ('9065C', '9065C'), ('C9065','C9065'), ('9065c','9065c'),
    ('c60', 'c60'), ('c70', 'c70'),('C70','C70'),('C75','C75'),
    ('C60','C60'), ('c75', 'c75'),('60C', '60C'),
    ('560', '560'), ('550', '550'),
    ('j60', 'j60'),
    ('D95','D95'), ('D125', 'D125'), 
    ('b7025', 'b7025'), ('b7030', 'b7030'), ('b7035', 'b7035'), ('7030', '7030'),
    ('7025B', '7025B'), ('7030B', '7030B'), ('7035B', '7035B'),
    ('7025b', '7025b'), ('7030b', '7030b'), ('7035b', '7035b'),
    ('5325', '5325'), ('5330', '5330'), ('5335', '5335'), ('5322', '5322'),
    ('4210', '4210'),
    ('5016', '5016'), ('5020', '5020'),
    ('5019', '5019'), ('5021', '5021'),
    ('5022', '5022'), ('5024', '5024'),
    ('5735', '5735'), ('5745', '5745'), ('5755', '5755'), ('5765', '5765'),('5775', '5775'), ('5790', '5790'),
    ('6532', '6532'),('5635', '5635'), ('5645', '5645'), ('5655', '5655'), ('5665', '5665'),('5675', '5675'), ('5690', '5690'),
    ('255', '255'), ('245', '245'), ('265', '265'), ('275', '275'),('55', '55'),('45', '45'),
    ('3655', '3655'),('3315','3315'), ('3325', '3325'),
    ('3415', '3415'), ('3420', '3420'), ('3425', '3425'),
    ('3430', '3430'), ('3435', '3435'), ('3450', '3450'),
    ('3600','3600'), ('3610', '3610'),
    ('4510', '4510'),
    ('5500', '5500'),
    ('4118', '4118'), ('M 20', 'M 20'),('M20', 'M20'),('M 15', 'M 15'),('M15', 'M15'),
    ('3635', '3635'),('3550','3550'),
    ('3210', '3210'),('3215', '3215'), ('3220', '3220'),('3230', '3230'),('3225', '3225'),('3250', '3250'), ('3260', '3260'),('3235', '3235'),
    ('3045', '3045'),
    ('3335','3335'), ('3320', '3320'),('3330','3330'),('3200','3200'),('3345', '3345'),
    
    ('3615', '3615'),('3020','3020'),('3025','3025'),('3030', '3030'), ('3040', '3040'), ('3045', '3045'),
    ('8880', '8880'), ('8870', '8870'),
    ('5222', '5222'),('5225', '5225'), ('5230', '5230'), ('5235', '5235'), ('5225A', '5225A'), ('5230A', '5230A'), ('5235A', '5235A'),
    ('118', '118'), ('128', '128'), ('133', '133'),
    ('4150', '4150'), ('4260', '4260'),('4250', '4250'),
    ('b405', 'b405'), ('c405', 'c405'),('405B', '405B'),('405C', '405C'),('B405', 'B405'), ('C405', 'C405'),
    ('c7025', 'c7025'), ('c7030', 'c7030'), ('c7035', 'c7035'),('7025C','7025C'), ('7030C',  '7030C'), ('7035C', '7035C'),
    ('b8045', 'b8045'), ('b8055', 'b8055'),('b8065', 'b8065'), ('b8075', 'b8075'), ('b8090', 'b8090'),
    ('8045B', '8045B'), ('8055B', '8055B'), ('8065B', '8065B'), ('8075B', '8075B'), ('8090B', '8090B'),
    ('8045b', '8045b'), ('8055b', '8055b'), ('8065b', '8065b'), ('8075b', '8075b'), ('8090b', '8090b'),
    ('c8035', 'c8035'), ('c8045', 'c8045'), ('c8055', 'c8055'), ('c8065', 'c8065'), ('c8075', 'c8075'),
    ('8030C', '8030C'), ('8035C', '8035C'), ('8045C', '8045C'), ('8055C', '8055C'), ('8065C', '8065C'), ('8075C', '8075C'),
    ('180', '180'), ('2100', '2100'), ('3100', '3100'), ('4100', '4100'), ('280','280'),('V180','V180'),
    ('9100B', '9100B'), ('b9100', 'b9100'), ('9100b', '9100b'),('B9100', 'B9100'),
    ('6204', '6204'), ('6705', '6705'),
    ('6180','6180'), ('412', '412'), ('315', '315'), ('420', '420'),

    )
    #response and return times
    production  = 4
    workcentre_radiology = 6
    phasor = 9
    production_return = 4
    production_return_meter = 2000
    office_radiology_return = 7
    office_return_meter = 5000
    radiology_return_meter = 5000
    #weekdays choices
    Saturday = 5
    Sunday = 6
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    NoDayoff = 7
    weekday_choices = ((Monday, 'Monday'),(Tuesday, 'Tuesday'),(Wednesday, 'Wednesday'),(Thursday, 'Thursday'),(Friday, 'Friday'),(Saturday, 'Saturday'),(Sunday, 'Sunday'),(NoDayoff, 'NoDayoff'))


    response_choices_hours = ((production, 'Production'),(workcentre_radiology, 'Workcentre/radiology'), (phasor, 'Phasor'))
    return_choices_days = ((production_return, 'Production'), (office_radiology_return, 'Office/radiology'))
    # name= models.CharField(max_length=200)
    serial = models.BigIntegerField('standard seial', help_text='fill this if your serial is numbers only', unique=True, blank=True)
    serial2 = models.CharField('non-standard serial', max_length=10, help_text="fill this if your serial consists of numbers and letters", unique=True,null=True, blank=True)
    machine_serial = models.CharField(max_length=12, null=True, blank=True)
    machine_full_serial = models.CharField(max_length=12, null=True, blank=True)
    # machine_model = models.CharField(max_length=100)
    machine_model =models.CharField(max_length=10, choices=model_choices, default='no model')
    # slug = models.SlugField(unique=True)
    machine_location = models.TextField(null=True, blank=True)
    installation_date = models.DateTimeField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    # speed = models.IntegerField(blank = True, null=True, choices=speed_choices)
    machine_points = models.FloatField(default=1)
    machine_response_time = models.IntegerField(choices=response_choices_hours, null=True, blank=True)
    machine_callback_time = models.IntegerField(choices=return_choices_days, null=True, blank=True) 
    begin_at = models.TimeField(default=datetime.time(hour=8, minute=0, second=0))
    finish_at = models.TimeField(default=datetime.time(hour=16, minute=0, second=0))
    #organization = models.ForeignKey(to='CustomerOrganization',on_delete=models.CASCADE, related_name='customers',null=True, blank=True)
    first_week_dayoff = models.IntegerField(choices=weekday_choices, default=7)
    second_week_dayoff = models.IntegerField(choices=weekday_choices, default=7)
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
    radiology = 'radiology'
    bw_production = 'mono production'
    color_production = 'color production'

    category_choices = ((bw_workcentre,'B/W workcentre'),(color_workcentre,'Color workcentre'), (bw_phasor,'B/W phasor'),
    (color_phasor,'Color phasor'), (wide_format,'Wide Format'), (bw_production, 'B/W production'), (color_production, 'Color production'), (radiology,'Radiology'))
    
    # category = models.ForeignKey(Category, on_delete=models.CASCADE,  blank=True, null=True)
    machine_category = models.CharField('Machine Category',max_length=100,choices=category_choices, blank=True,null=True)
    customer = models.ForeignKey(Customer,related_name='machines', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='machines_dep', on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, related_name='machines', on_delete=models.CASCADE, blank=True,null=True)
    # engineers = models.ManyToManyField(Engineer, related_name='machines', blank=True)
    contract = models.OneToOneField(to='Contract', on_delete=models.DO_NOTHING, related_name='machine', null=True, blank=True)
    #contact = models.ForeignKey(to='MachineContact', on_delete=models.CASCADE,related_name='')
    #call = models.OneToOneField()
    objects = models.Manager()
    objects1 = MachineManager()
    class Meta:
        unique_together = ['serial', 'machine_model']

    def __str__(self):
        if hasattr(self.department,'department_name'):
            return '{}'.format(self.serial) + ' ' +self.machine_model + "  " + self.department.department_name
        else:
            return '{}'.format(self.serial) + ' ' +self.machine_model
    # def save(self,*args,**kwargs):
    #     department = Department.objects.get(pk=self.department.id)
    #     department.no_of_machine +=1

    #     department.save(update_fields=['no_of_machine'])
    #     self.department = department
    #     super().save(*args,**kwargs)
class Call(models.Model):
    #from machine.models import Machine
    unassigned = 'unassigned'
    incomplete = 'incomplete'
    completed =  'completed'
    dispatched =  'dispatched'
    status_choices = ((unassigned, 'Unassigned'),(dispatched, 'Dispatched'), (incomplete, 'Incomplete'),(completed, 'Completed'))
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
    
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    response_time_end_date= models.DateTimeField(null=True,blank=True)
    response_time_tail_end_date = models.DateTimeField(null=True,blank=True)
    down_time_end_date = models.DateTimeField(null=True, blank=True)    
    assigned_date = models.DateTimeField(blank=True, null=True)
    optimum_completed_date = models.DateTimeField(help_text="the default value is 6 hours + assign_date", null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    real_assigned_date=models.DateTimeField(null=True, blank=True)
    real_completed_date = models.DateTimeField(null=True, blank=True)
    start_of_call = models.DateTimeField(null=True, blank=True)
    first_time_finish = models.BooleanField(default=False)
    callback_call = models.BooleanField(default=False)
    response_success_call = models.BooleanField(default=False)
    response_tail_success_call = models.BooleanField(default=False)
    down_success_call = models.BooleanField(default=False)
    down_time = models.DurationField(null=True, blank=True)
    response_time = models.DurationField(null=True, blank=True)

    delayed_call = models.BooleanField(default=False)
    no_of_visits = models.IntegerField(default=0)
    
    

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
        # indexes=['notification_number']
    def __str__(self):
        if self.engineer:
                return (Engineer.objects.get(id=self.engineer.id).name) + ' ' + self.machine.customer.name + ' ' + self.machine.machine_model + ' ' +str(self.notification_number)
        return self.machine.machine_model + ' ' + self.machine.customer.name + ' ' + str(self.notification_number) + ' ' + ' no engineer assigned yet'
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
    incomplete = 'incomplete'
    completed =  'completed'
    status_choices = ((incomplete, 'Incomplete'),(completed, 'Completed'))

    call = models.ForeignKey(Call, related_name='reports', on_delete=models.CASCADE)
    # customer_name = models.CharField(max_length=50,default='')
    engineer = models.ForeignKey(Engineer,related_name='calls', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=status_choices, default=incomplete)

    # notification_number = models.IntegerField(null=True, blank=True)
    # machine_serial = models.IntegerField(blank=True, null=True)
    billing_meter_black = models.IntegerField(null=True, blank=True, default=0)
    billing_meter_color = models.IntegerField(null=True, blank=True, default=0)
    billing_meter_total = models.IntegerField(null=True, blank=True, default=0)

    billing_meter1 = models.IntegerField(null=True, blank=True, default=0)
    billing_meter2 = models.IntegerField(null=True, blank=True, default=0)
    
    report_copy = models.FileField(upload_to='files/reports/', blank=True, null=True)
    
    image = models.ImageField(upload_to='images/reports/', blank=True, null=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    finishs_at = models.DateTimeField(blank=True, null=True)

    summary = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
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
    warranty = 'Warranty'
    contract_choices=((fsma, 'FSMA'), (labour, 'Time'), (lis,'LIS'),(fm, 'FM'), (xpps,'XPPS'), (tandm, 'T&M'), (warranty, 'Warranty'))
    
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
        if self.contract_type:
            return self.contract_type + ' {}'.format(self.machine_serial)
        else:
            return '{}'.format(self.machine_serial)
    



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
        return self.image_name + ' ' + self.review.machine.machine_model + ' ' +self.review.review_title


class FileReview(models.Model):
    review = models.ForeignKey(EngineerReview, related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name + ' ' + self.review.machine_model + ' ' +self.review.review_title


class ImageReport(ImageAbstract):
    report = models.ForeignKey(Report, related_name='report_images', on_delete=models.CASCADE)


    def __str__(self):
        if self.image_name:

            return self.image_name + ' ' + str(self.report.call.notification_number)
        else:
            return str(self.report.call.notification_number)


class FileReport(FileAbstract):
    Report = models.ForeignKey(Report, related_name='report_files', on_delete=models.CASCADE)


    def __str__(self):
        return self.file_name + ' ' + self.report.call.notification_number

class Contact(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contact', null=True, blank=True)
    first_name = models.CharField('First name', max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    mobile = models.IntegerField()
    telephone = models.PositiveIntegerField(null=True, blank=True)
    email_address = models.EmailField(null=True,blank=True)
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='call_contacts')

class MachineContact(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contact', null=True, blank=True)
    first_name = models.CharField('First name', max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    mobile = models.IntegerField()
    telephone = models.PositiveIntegerField(null=True, blank=True)
    email_address = models.EmailField(null=True,blank=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='machine_contacts')



    def __str__(self):
        # if self.user is None:
        #     return self.first_name + " " +self.last_name
        # else:
        #     return self.first_name + " " +self.last_name + " " + self.user.username
        return self.first_name+ ''+self.last_name



