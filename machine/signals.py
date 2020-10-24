from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Call, Machine, Contract
from customer.models import Department
import datetime
from django.utils import timezone
from django.db import transaction
from dateutil.relativedelta import relativedelta

workcentre_black_category = ['b7025', 'b7030', 'b7035',
'b405',
'b8045', 'b8055', 'b8065',
'5945', '5955',
'5325', '5330', '5335', 
'5225', '5230', '5235', '5225A', '5230A', '5235A',
'128', '133',
'4150', '4260',
'255', '265', '275', '245',
'5635', '5645', '5655', '5665', '5690',
'5735', '5745', '5755', '5765', '5790',
]
workcentre_color_category = [
     'c7025', 'c7030', 'c7035',
     'c8035', 'c8045', 'c8055', 'c8065', 'c8075',
     'c405',
     '7225', '7220',
     '7120',
     '7835', '7845', '7855',
     '7990',
     'c605',

]
phasor_black_category = ['3615', '3655', '3635', '3310', '3315']
phasor_color_category = []
radiology_category = ['c60', '550', '560']
production_color_category = ['180', '2100', '3100']
production_black_category = []

@receiver(post_save, sender=Machine)
def handle_machine_save(sender, instance, created, **kwargs):
        if created:
                print('1')
                if instance.machine_model:
                        if instance.machine_model in workcentre_black_category:
                                print('2')
                                instance.machine_category = 'mono workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                pass
                        elif instance.machine_model in workcentre_color_category:
                                print('3')
                                instance.machine_category = 'color workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                pass
                        elif instance.machine_model in phasor_black_category:
                                print('4')
                                instance.machine_category = 'mono phasor'
                                instance.machine_response_time = 9
                                instance.machine_callback_time = 7
                                pass
                        elif instance.machine_model in phasor_color_category:
                                print('5')
                                instance.machine_category = 'color phasor'
                                instance.machine_response_time = 9
                                instance.machine_callback_time = 7
                                pass
                        elif instance.machine_model in radiology_category:
                                print('6')
                                instance.machine_category = 'radiology'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                pass
                        elif instance.machine_model in production_black_category:
                                print('7')
                                instance.machine_category = 'mono production'
                                instance.machine_response_time = 4
                                instance.machine_callback_time = 4
                                pass
                        elif instance.machine_model in production_color_category:
                                print('8')
                                instance.machine_category = 'color production'
                                instance.machine_response_time = 4
                                instance.machine_callback_time = 4
                                pass
                        else:
                                print('9')
                                pass


                department = Department.objects.get(pk=instance.department.id)
                department.no_of_machine +=1

                department.save(update_fields=['no_of_machine'])
                instance.department = department
                if instance.customer:
                        if instance.customer.organization:
                                instance.customer.organization.save(update_fields=['organization_machines_number'])
                        
                if instance.contract and instance.contract.contract_type != 'Warranty':
                        print('h3')
                        contract = Contract.objects.get(id=instance.contract.id)
                        contract.machine_serial=instance.serial
                        # instance.contract = 
                        contract.save(update_fields=['machine_serial'])
                if instance.contract and instance.installation_date:
                        print(instance.installation_date, instance.added)
                        x = instance.installation_date.date() == instance.added.date()
                        y = instance.installation_date + datetime.timedelta(days=365) >= datetime.datetime.now(timezone.utc)
                        print(instance.installation_date.date, instance.added.date)
                        print(x)
                        if x:
                                print('123')
                                # if instance.installation_date + datetime.timedelta(days=365) < datetime.datetime.now():
                                print('contact here warranty')
                                c = Contract.objects.create(contract_type='Warranty', machine_serial=instance.serial, monthly_fees=0)
                                print(c.contract_type)
                                print(instance.installation_date, instance.added)
                                print(x)
                                instance.contract = c
                                instance.save()
                        elif y:
                                c = Contract.objects.create(contract_type='Warranty', machine_serial=instance.serial, monthly_fees=0)
                                c.start_of_contract=instance.installation_date
                                c.end_of_contract=instance.installation_date + datetime.timedelta(days=365)
                                c.save(update_fields=['start_of_contract', 'end_of_contract'])
                                instance.contract = c
                                instance.save()

        else:
                if instance.contract is not None:
                        print('h4')
                        contract = Contract.objects.get(id=instance.contract.id)
                        contract.machine_serial=instance.serial
                        contract.save(update_fields=['machine_serial'])
@receiver(post_delete, sender=Machine)
def handle_delete_machine(sender, instance, using, **kwargs):

        department = Department.objects.get(pk=instance.department.id)
        department.no_of_machine -=1

        department.save(update_fields=['no_of_machine'])
        instance.department = department
        if instance.customer:
                if instance.customer.organization:
                        instance.customer.organization.save(update_fields=['organization_machines_number'])



previous_state = ""
@receiver(post_save, sender=Call)
def handle_call_save(sender,instance,created, **kwargs):
        weekday_choices =['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

        if created:
                if instance.engineer:

                        instance.is_assigned=True
                        # call = kwargs.get('instance')
                        instance.status='dispatched'
                        instance.assigned_date = datetime.datetime.now()
                        print(instance.assigned_date.weekday())
                        assigned_date_only = instance.assigned_date.date()
                        assigned_time_real = datetime.time(8,0)
                        result_date = datetime.datetime.combine(assigned_date_only, assigned_time_real)
                        

                        if instance.assigned_date.weekday() in [0, 1, 2, 3, 6]:
                                if instance.customer.first_week_dayoff in [7,4,5] and instance.customer.second_week_dayoff in [7,4,5]:
                                        instance.real_assigned_date = instance.assigned_date
                                elif (instance.assigned_date.weekday() == instance.customer.first_week_dayoff and instance.customer.second_week_dayoff != instance.customer.first_week_dayoff + 1) or (instance.assigned_date.weekday() == instance.customer.second_week_dayoff and instance.customer.first_week_dayoff != instance.customer.second_week_dayoff + 1):
                                        instance.real_assigned_date = instance.assigned_date + datetime.timedelta(days=1)
                                elif (instance.assigned_date.weekday() == instance.customer.first_week_dayoff and instance.customer.second_week_dayoff == instance.customer.first_week_dayoff + 1) or (instance.assigned_date.weekday() == instance.customer.second_week_dayoff and instance.customer.first_week_dayoff == instance.customer.second_week_dayoff + 1):
                                        instance.real_assigned_date = instance.assigned_date + datetime.timedelta(days=1)
                                else:
                                        instance.real_assigned_date = instance.assigned_date                                        
                        elif instance.assigned_date.weekday() == 4:
                                
                                if instance.customer.first_week_dayoff in [7,1,2,3,0,4,5] and instance.customer.second_week_dayoff in [7,1,2,3,0,4,5]:

                                        instance.real_assigned_date = result_date + datetime.timedelta(days=2)
                                elif instance.customer.first_week_dayoff == 6 and instance.customer.second_week_dayoff == 0:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=4)                                
                                else:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=3)
                        elif instance.assigned_date.weekday() == 5:
                                if instance.customer.first_week_dayoff in [7,1,2,3,0,4,5] and instance.customer.second_week_dayoff in [7,1,2,3,0,4,5]:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=1)
                                        print('route1', instance.customer.first_week_dayoff, instance.customer.second_week_dayoff)
                                elif instance.customer.first_week_dayoff == 6 and instance.customer.second_week_dayoff == 0:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=3)                                
                                
                                else:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=2)
                                        print('route2')
                        else:
                                instance.real_assigned_date = instance.assigned_date


                        # elif instance.assigned_date.weekday()!= 4 and instance.assigned_date.weekday() !=5 and instance.customer.first_week_dayoff
                       



                        # instance.previous_status = instance.status
                        engineer = instance.engineer
                        
                        engineer.no_of_calls += 1
                        engineer.no_of_calls_dispatched += 1
                        # engineer.no_of_calls_pending += 1
                        engineer.save()
                        instance.engineer = engineer
                        instance.previous_engineer=instance.engineer
                        instance.previous_status = instance.status
    
                        # print(instance.status)
                        instance.save()
                        return
                else:
                        instance.status = 'unassigned'
                        instance.previous_status = 'unassigned'
                        instance.is_assigned = False

                        instance.save()
                        return

        else:

                if instance.status == 'completed' and instance.previous_status!='completed':
                        if instance.engineer and instance.previous_status=='incomplete':
                                engineer = instance.engineer
                                engineer.no_of_calls_pending -= 1
                                engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched

                                # engineer.no_ofcalls_success +=1
                                engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success'])
                                instance.engineer = engineer
                                instance.previous_status = instance.status
                                instance.completed_date = datetime.datetime.now()
                                instance.save(update_fields=['engineer', 'previous_status', 'completed_date'])
                        elif instance.engineer and instance.previous_status=='dispatched':
                                engineer = instance.engineer
                                engineer.no_of_calls_dispatched -= 1
                                engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - - engineer.no_of_calls_dispatched

                                # engineer.no_ofcalls_success +=1
                                engineer.save(update_fields=['no_of_calls_dispatched', 'no_ofcalls_success'])
                                instance.engineer = engineer
                                instance.previous_status = instance.status
                                instance.completed_date = datetime.datetime.now()
                                instance.save(update_fields=['engineer', 'previous_status', 'completed_date'])
                elif instance.status == 'dispatched' and instance.previous_status!='dispatched':
                        if instance.previous_status=='unassigned':
                                print('iam here1')
                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        print('iam here2')
                                        engineer = instance.engineer
                                        engineer.no_of_calls += 1
                                        engineer.no_of_calls_dispatched += 1
                                        engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending-engineer.no_of_calls_dispatched

                                        engineer.save(update_fields=['no_of_calls_dispatched', 'no_of_calls', 'no_ofcalls_success'])
                                        instance.previous_status = instance.status
                                        instance.is_assigned = True
                                        instance.assigned_date = datetime.datetime.now()
                                        


                                        instance.save(update_fields=['engineer', 'is_assigned', 'previous_status', 'assigned_date'])

                elif instance.status == 'dispatched' and instance.previous_status=='dispatched':
                        print('newhererrreerr')
                        if instance.engineer != instance.previous_engineer:
                                previous_engineer = instance.previous_engineer
                                previous_engineer.no_of_calls -= 1
                                previous_engineer.no_of_calls_dispatched -=1
                                previous_engineer.save(update_fields=['no_of_calls', 'no_of_calls_dispatched'])
                                engineer = instance.engineer
                                engineer.no_of_calls +=1
                                engineer.no_of_calls_dispatched += 1
                                engineer.save(update_fields=['no_of_calls', 'no_of_calls_dispatched'])
                                instance.previous_engineer = engineer
                                # instance.assigned_date = datetime.datetime.now()
                                instance.save(update_fields=['previous_engineer'])
                elif instance.status == 'unassigned':
                        if instance.previous_status != 'unassigned':
                                if instance.is_assigned == True:
                                        if instance.engineer and instance.engineer!='no engineer assigned yet':
                                                engineer = instance.engineer
                                                
                                                engineer.no_of_calls -= 1

                                                if instance.previous_status == 'dispatched':
                                                        engineer.no_of_calls_dispatched -= 1
                                                        engineer.no_of_calls_pending = engineer.no_of_calls_pending
                                                        engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched

                                                elif instance.previous_status == 'incomplete':
                                                
                                                        engineer.no_of_calls_pending -= 1

                                                        engineer.no_of_calls_dispatched = engineer.no_of_calls_dispatched
                                                        engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched

                                                engineer.save(update_fields=['no_of_calls_pending', 'no_of_calls', 'no_ofcalls_success', 'no_of_calls_dispatched'])
                                                instance.engineer = None
                                                instance.assigned_date = None
                                                instance.previous_status = instance.status
                                                instance.is_assigned = False
                                                instance.save(update_fields=['engineer', 'is_assigned', 'previous_status', 'assigned_date'])
                        else:

                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        print('iam hereeeeee')
                                        engineer = instance.engineer
                                        engineer.no_of_calls += 1
                                        engineer.no_of_calls_dispatched += 1

                                        engineer.save(update_fields=['no_of_calls', 'no_of_calls_dispatched'])
                                        instance.is_assigned=True
                                        instance.previous_engineer = engineer
                                        instance.status='dispatched'
                                        instance.previous_status = 'dispatched'
                                        instance.assigned_date = datetime.datetime.now()
                                        assigned_date_only = instance.assigned_date.date()
                                        assigned_time_real = datetime.time(8,0)
                                        result_date = datetime.datetime.combine(assigned_date_only, assigned_time_real)


                                        if instance.assigned_date.weekday() in [0, 1, 2, 3, 6]:
                                                if instance.customer.first_week_dayoff in [7,4,5] and instance.customer.second_week_dayoff in [7,4,5]:
                                                        instance.real_assigned_date = instance.assigned_date
                                                elif (instance.assigned_date.weekday() == instance.customer.first_week_dayoff and instance.customer.second_week_dayoff != instance.customer.first_week_dayoff + 1) or (instance.assigned_date.weekday() == instance.customer.second_week_dayoff and instance.customer.first_week_dayoff != instance.customer.second_week_dayoff + 1):
                                                        instance.real_assigned_date = instance.assigned_date + datetime.timedelta(days=1)
                                                elif (instance.assigned_date.weekday() == instance.customer.first_week_dayoff and instance.customer.second_week_dayoff == instance.customer.first_week_dayoff + 1) or (instance.assigned_date.weekday() == instance.customer.second_week_dayoff and instance.customer.first_week_dayoff == instance.customer.second_week_dayoff + 1):
                                                        instance.real_assigned_date = instance.assigned_date + datetime.timedelta(days=1)
                                                else:
                                                        instance.real_assigned_date = instance.assigned_date                                        
                                        elif instance.assigned_date.weekday() == 4:
                                
                                                if instance.customer.first_week_dayoff in [7,1,2,3,0,4,5] and instance.customer.second_week_dayoff in [7,1,2,3,0,4,5]:

                                                        instance.real_assigned_date = result_date + datetime.timedelta(days=2)
                                                elif instance.customer.first_week_dayoff == 6 and instance.customer.second_week_dayoff == 0:
                                                        instance.real_assigned_date = result_date + datetime.timedelta(days=4)                                
                                                else:
                                                        instance.real_assigned_date = result_date + datetime.timedelta(days=3)
                                        elif instance.assigned_date.weekday() == 5:
                                                if instance.customer.first_week_dayoff in [7,1,2,3,0,4,5] and instance.customer.second_week_dayoff in [7,1,2,3,0,4,5]:
                                                        instance.real_assigned_date = result_date + datetime.timedelta(days=1)
                                                        print('route1', instance.customer.first_week_dayoff, instance.customer.second_week_dayoff)
                                                elif instance.customer.first_week_dayoff == 6 and instance.customer.second_week_dayoff == 0:
                                                        instance.real_assigned_date = result_date + datetime.timedelta(days=3)                                
                                
                                                else:
                                                        instance.real_assigned_date = result_date + datetime.timedelta(days=2)
                                                        print('route2')
                                        else:
                                                instance.real_assigned_date = instance.assigned_date
                                        instance.save(update_fields=['engineer','previous_engineer', 'is_assigned', 'status', 'previous_status', 'assigned_date','real_assigned_date'])



                elif instance.status =='incomplete' and instance.previous_status != 'incomplete':
                        if instance.is_assigned == True:
                                if instance.engineer and instance.engineer != 'no engineer assigned yet':
                                        engineer = instance.engineer
                                        if instance.previous_status:
                                                if instance.previous_status == 'dispatched':
                                                        
                                                        #engineer.no_of_calls +=1
                                                        engineer.no_of_calls_pending += 1
                                                        engineer.no_of_calls_dispatched -= 1
                                                        engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched
                                                        engineer.save(update_fields=['no_of_calls_pending','no_of_calls_dispatched', 'no_ofcalls_success','no_of_calls'])
                                                                        
                                
                                                # engineer.no_of_calls +=1
                                                # engineer.no_of_calls_pending += 1
                                                # engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending
                                                # engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success','no_of_calls'])
                                        else:
                                                engineer.no_of_calls_pending += 1
                                                engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched
                                                engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success'])
                                        instance.engineer = engineer
                                        instance.previous_status = instance.status
                                        instance.save(update_fields=['engineer', 'previous_status'])
                                else:
                                        engineer = instance.engineer
                                        engineer.no_of_calls +=1
                                        engineer.no_of_calls_pending += 1
                                        engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending
                                        engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success', 'no_of_calls'])
                                        instance.engineer = engineer
                                        instance.previous_status = instance.status
                                        instance.save(update_fields=['engineer', 'previous_state'])
 

                                        
                        else:
                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        engineer = instance.engineer
                                        engineer.no_of_calls +=1
                                        engineer.no_of_calls_pending += 1
                                        engineer.save(update_fields=['no_of_calls_pending', 'no_of_calls'])
                                        instance.engineer = engineer
                                        instance.previous_status = instance.status
                                        instance.save(update_fields=['engineer','previous_status'])
                                else:
                                        instance.status='unassigned'
                                        instance.previous_status='unassigned'
                                        instance.save(update_fields=['status', 'previous_status'])
                                        
                                        

                                
        #             instance.engineer = engineer
        #             instance.is_assigned = False
        #             instance.save()
        # elif instance.status == 'pending':
        #     if instance.is_assigned == False:
        #         engineer = instance.engineer
        #         engineer.no_of_calls += 1
        #         engineer.no_of_calls_pending += 1
        #         engineer.save(force_update=True)
        #         instance.engineer = engineer
        #         instance.is_assigned = False
        #         instance.save()


@receiver(post_save, sender=Contract)
def handle_contract_save(sender,instance, created,**kwargs):
        if created:
                # if instance.machine:
                        if instance.contract_type == 'T&M':
                                instance.monthly_fees = 0.0
                        if instance.start_of_contract is None:
                                instance.start_of_contract = datetime.now()
                        if instance.start_of_contract:
                                instance.end_of_contract=instance.start_of_contract + relativedelta(years=1)
                        try:

                                if instance.machine:
                                        instance.machine_serial = instance.machine.serial
                                        instance.save()

                        except:
                                instance.machine_serial =0
                                instance.save()
                                
                        # if instance.machine. is None:

                        #         instance.machine_serial = instance.machine.serial
                        #         instance.save()
        # else:
        #         try:

        #                 if instance.machine:
        #                         instance.machine_serial = instance.machine.serial
        #                         instance.save(update_fields=['machine_serial'])

        #         except:
        #                 instance.machine_serial =3
        #                 instance.save(update_fields=['machine_serial'])
        #         # if hasattr(instance, 'machine'):
        #                 try:
        #                         machine_contract = Machine.objects.get(contract__id=instance.id)
        #                         if machine_contract:
        #                                 print('there is a machine')                   
        #                         if instance.machine:
        #                                 print('h1')
        #                                 with transaction.atomic():
        #                                         # instance.machine_serial = instance.machine.serial
        #                                         machine = Machine.objects.get(serial=instance.machine.serial)
        #                                         print('{}--{}'.format(instance.machine_serial, machine.serial))
        #                                         # instance.machine = machine
        #                                         instance.machine_serial = machine.serial                                                                                                
        #                                         print('{}--{}'.format(instance.machine_serial, machine.serial))

        #                                         # instance.save()
        #                                         print('{}--{}'.format(instance.machine_serial, machine.serial))


        #                 except:
        #                         print('h2')
        #                         instance.machine_serial = 1
        #                         # instance.save(update_fields=['machine_serial'])
        #                 # instance.save()