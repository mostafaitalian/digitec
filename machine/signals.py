from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Call, Machine, Contract, Report
from customer.models import Department
import datetime
from django.utils import timezone
from django.db import transaction
from dateutil.relativedelta import relativedelta
from functools import wraps
import datetime
import pytz
import businesstimedelta
import holidays as pyholidays
from .helpers import send_push_message

utc=pytz.UTC
egy = pytz.timezone('Africa/Cairo')

working = businesstimedelta.WorkDayRule(start_time=datetime.time(8), end_time=datetime.time(16), working_days=[0,1,2,3,6],tz=pytz.timezone('Africa/Cairo'))
working_days_hrs = working
def tz_aware(dt):
        return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None
def convert_to_utc_aware(dt):
        out = dt
        try:
                out = dt.astimezone(pytz.utc)
        except (ValueError, TypeError) as exc:
                out = dt.replace(tzinfo=pytz.utc)
        return out

        

def skip_signal():
        def _skip_signal(signal_func):
                @wraps(signal_func)
                def _decorator(sender, instance, **kwargs):
                        if(hasattr(instance, 'skip_signal')):
                                return None
                        return signal_func(sender, instance, **kwargs)
                return _decorator
        return _skip_signal
workcentre_black_category_s = [
        'b405','405B', '405b',
        '4150', '4260',
        '3550',  '3655', '3635',
        'B605','B615', '605B', '615B', 'b605', 'b615',
        '5016','5020', '5019', '5021', '5022', '5024',
        '1022B', '1025B', 'b1022', 'b1025',

]
workcentre_black_category_m = [
        'b7025', 'b7030', 'b7035',
        '7025B', '7030B', '7035B',
        '7025b', '7030b', '7035b',


        '5325', '5330', '5335', 
        '5225', '5230', '5235', '5225A', '5230A', '5235A',
        '128', '133',
]
workcentre_black_category_l = [
        '255', '265', '275', '245',
        '5635', '5645', '5655', '5665', '5690',
        '5735', '5745', '5755', '5765', '5790',
        'b8045', 'b8055', 'b8065', '8045B', '8055B', '8065B', '8045b', '8055b', '8065b',
        '5945', '5955',
        '5855', '5845', '5865', '5890',
]
workcentre_color_category_s = [
        'c405', '405C',
        'c605', '605C',
]
workcentre_color_category_m = [
     'c7025', 'c7030', 'c7035','7025C', '7030C', '7035C',
     

     '7225', '7220', '7230', '7221',
     '7120', '7125', '7132', '7232','7242',
     '6655',




]
workcentre_color_category_l = [

        '7835', '7845', '7855',
        '7990',
        'c8030', 'c8035', 'c8045', 'c8055', 'c8065', 'c8075', '8035C', '8030C', '8045C', '8055C', '8065C',

]
phasor_black_category = ['3615','3310', '3315','3600', '3320', '3330', '3325', '3200']
phasor_color_category = ['8880', '8870',]
radiology_category = ['c60', '550', '560', 'c70', 'j70','c9065', 'c75', 'C75']
production_color_category = ['180', '2100', '3100','280', '4100', 'V180']
production_black_category = ['D95',]
wide_format_category = ['6204', '6705']
@receiver(post_save, sender=Machine)
@skip_signal()
def handle_machine_save(sender, instance, created, **kwargs):
        if created:
                print('1')
                if instance.machine_model:
                        if instance.machine_model in workcentre_black_category_s:
                                print('2')
                                instance.machine_category = 'mono workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points = 0.8
                                pass
                        elif instance.machine_model in workcentre_black_category_m:
                                print('2')
                                instance.machine_category = 'mono workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points = 1
                                pass
                        elif instance.machine_model in workcentre_black_category_l:
                                print('2')
                                instance.machine_category = 'mono workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points = 1.4
                                pass
                        elif instance.machine_model in workcentre_color_category_s:
                                print('3')
                                instance.machine_category = 'color workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points = 1
                                pass
                        elif instance.machine_model in workcentre_color_category_m:
                                print('3')
                                instance.machine_category = 'color workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points = 1.2
                                pass
                        elif instance.machine_model in workcentre_color_category_l:
                                print('3')
                                instance.machine_category = 'color workcentre'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points = 2
                                pass
                        elif instance.machine_model in phasor_black_category:
                                print('4')
                                instance.machine_category = 'mono phasor'
                                instance.machine_response_time = 9
                                instance.machine_callback_time = 7
                                instance.machine_points = 0.6
                                pass
                        elif instance.machine_model in phasor_color_category:
                                print('5')
                                instance.machine_category = 'color phasor'
                                instance.machine_response_time = 9
                                instance.machine_callback_time = 7
                                instance.machine_points = 0.8
                                pass
                        elif instance.machine_model in radiology_category:
                                print('6')
                                instance.machine_category = 'radiology'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points =  2
                                pass
                        elif instance.machine_model in production_black_category:
                                print('7')
                                instance.machine_category = 'mono production'
                                instance.machine_response_time = 4
                                instance.machine_callback_time = 4
                                instance.machine_points = 2
                                pass
                        elif instance.machine_model in production_color_category:
                                print('8')
                                instance.machine_category = 'color production'
                                instance.machine_response_time = 4
                                instance.machine_callback_time = 4
                                instance.machine_points = 2
                                pass
                        elif instance.machine_model in wide_format_category:
                                instance.machine_category = 'wide format'
                                instance.machine_response_time = 6
                                instance.machine_callback_time = 7
                                instance.machine_points =  1.6
                        else:
                                print('9')
                                pass

                instance.skip_signal = True
                instance.save(update_fields=['machine_callback_time','machine_response_time','machine_category',])

                department = Department.objects.get(pk=instance.department.id)
                department.no_of_machine +=1

                department.save(update_fields=['no_of_machine'])
                instance.department = department
                # if instance.customer:
                #         if instance.customer.organization:
                #                 instance.customer.organization.save(update_fields=['organization_machines_number'])
                        
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
                pass
                # if instance.machine_model:
                #         if instance.machine_model in workcentre_black_category:
                #                 print('22')
                #                 instance.machine_category = 'mono workcentre'
                #                 instance.machine_response_time = 6
                #                 instance.machine_callback_time = 7
                #                 # instance.save()
                #                 # instance.save(update_fields=['machine_category'])
                #         elif instance.machine_model in workcentre_color_category:
                #                 print('3')
                #                 instance.machine_category = 'color workcentre'
                #                 instance.machine_response_time = 6
                #                 instance.machine_callback_time = 7
                #         elif instance.machine_model in phasor_black_category:
                #                 print('4')
                #                 instance.machine_category = 'mono phasor'
                #                 instance.machine_response_time = 9
                #                 instance.machine_callback_time = 7
                #         elif instance.machine_model in phasor_color_category:
                #                 print('5')
                #                 instance.machine_category = 'color phasor'
                #                 instance.machine_response_time = 9
                #                 instance.machine_callback_time = 7
                #         elif instance.machine_model in radiology_category:
                #                 print('6')
                #                 instance.machine_category = 'radiology'
                #                 instance.machine_response_time = 6
                #                 instance.machine_callback_time = 7
                #         elif instance.machine_model in production_black_category:
                #                 print('7')
                #                 instance.machine_category = 'mono production'
                #                 instance.machine_response_time = 4
                #                 instance.machine_callback_time = 4
                #         elif instance.machine_model in production_color_category:
                #                 print('8')
                #                 instance.machine_category = 'color production'
                #                 instance.machine_response_time = 4
                #                 instance.machine_callback_time = 4
                #         else:
                #                 print('9')
                # print(instance.machine_category)
                # instance.skip_signal = True
                # instance.save(update_fields=['machine_callback_time','machine_response_time','machine_category',])

                        #instance.save()
                # if instance.contract is not None:
                #         print('h4')
                #         contract = Contract.objects.get(id=instance.contract.id)
                #         contract.machine_serial=instance.serial
                #         contract.save(update_fields=['machine_serial'])
# @receiver(post_delete, sender=Machine)
# def handle_delete_machine(sender, instance, using, **kwargs):

#         department = Department.objects.get(pk=instance.department.id)
#         department.no_of_machine -=1

#         department.save(update_fields=['no_of_machine'])
#         instance.department = department
        # if instance.customer:
        #         if instance.customer.organization:
        #                 instance.customer.organization.save(update_fields=['organization_machines_number'])




# #previous_state = ""
# @receiver(post_save, sender=Call)
# def handlee_call_save(sender,instance,created, **kwargs):
#         weekday_choices =['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
#         working_hours = [8, 9, 10, 11, 12, 13, 14, 15]
#         working_weekday_choices = ['Friday', 'Saturday']
#         if created:
#                 checked_created_date = datetime.datetime.now()
#                 if checked_created_date.weekday() in [0,1,2,3,6] and checked_created_date.hour in working_hours:
#                         instance.created_date = checked_created_date
#                         instance.save(update_fields=['created_date'])
#                 if checked_created_date.weekday() in [4,5]:
#                         checked_created_date_date = checked_created_date.date()
#                         checked_created_date_time = checked_created_date_time()

#                         if checked_created_date.weekday() == 4:
#                                 checked_created_date_date = checked_created_date_date + datetime.timedelta(days=2)
#                                 checked_created_date_time = datetime.time(hour=8, minute=0)
#                                 modified_checked_created_date = datetime.datetime.combine(checked_created_date_date, checked_created_date_time)
#                                 instance.created_date = modified_checked_created_date
#                                 instance.save(update_fields=['created_date'])
#                         if checked_created_date.weekday() == 5:
#                                 checked_created_date_date = checked_created_date_date + datetime.timedelta(days=1)
#                                 checked_created_date_time = datetime.time(hour=8, minute=0)
#                                 modified_checked_created_date = datetime.datetime.combine(checked_created_date_date, checked_created_date_time)
#                                 instance.created_date = modified_checked_created_date
#
# 
#                                  instance.save(update_fields=['created_date'])

@receiver(post_save, sender=Call)
@skip_signal()
def handle_call_save(sender,instance,created, **kwargs):
        # weekday_choices =['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

        if created:
                r_t = datetime.datetime.now(timezone.utc)
                # instance.save(update_fields=['created_date'])
                print('hghg')
                
                if r_t.weekday() in [0,1,2,3,6] and r_t.hour < 16:
                        instance.created_date = datetime.datetime.now(timezone.utc)
                        print('1', instance.created_date.hour, '1111')
                elif r_t.weekday() in [0,1,2,6] and r_t.hour > 15:
                        instance.created_date = datetime.datetime.combine(r_t.date() + datetime.timedelta(days=1), datetime.time(8,0),timezone.utc) 
                        print('2')

                        
                elif r_t.weekday() in [0,1,2,3,6] and r_t.hour < 8:
                        instance.created_date = datetime.datetime.combine(r_t.date(), datetime.time(8,0), timezone.utc) 
                        print('2')                       
                elif r_t.weekday()==3 and r_t.hour > 15:
                        instance.created_date = datetime.datetime.combine(r_t.date() + datetime.timedelta(days=3), datetime.time(8,0), timezone.utc)
                        print('3')
                else:
                        print('else', r_t.weekday())
                        if r_t.weekday()==4:
                                time = datetime.time(8,0)
                                date = r_t.date() + datetime.timedelta(days=2)
                                instance.created_date = datetime.datetime.combine(date, time, timezone.utc)
                                        
                                                
                        elif r_t.weekday()==5:
                                time = datetime.time(8,0)
                                date = r_t.date() + datetime.timedelta(days=1)
                                instance.created_date = datetime.datetime.combine(date, time, timezone.utc)
                                # instance.save(update_fields=['created_date'])
                instance.save(update_fields=['created_date'])
                if instance.created_date:
                        instance.response_time_end_date = egy.localize(instance.created_date) + businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=instance.machine.machine_response_time)
                        #print(instance.created_date.replace(tzinfo=utc),businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=instance.machine.machine_response_time))
                        instance.response_time_tail_end_date = egy.localize(instance.created_date) + businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=instance.machine.machine_response_time*1.5)
                        instance.down_time_end_date = egy.localize(instance.created_date) + businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=12)
  
                        # r_e = instance.created_date + datetime.timedelta(hours=instance.machine.machine_response_time)
                        # r_t_e = instance.created_date + datetime.timedelta(minutes=instance.machine.machine_response_time*60*1.5)
                        # d_e = instance.created_date + datetime.timedelta(hours=12)
                        # if r_e.hour < 16 and instance.created_date.weekday() in [0,1,2,3,6]:
                        #         instance.response_time_end_date = instance.created_date + datetime.timedelta(hours=instance.machine.machine_response_time)        
                        # else:
                        #         if r_e.hour > 15 and instance.created_date.weekday() in [0,1,2,6]:
                                        
                        #                 instance.response_time_end_date = r_e + datetime.timedelta(days=1, hours=r_e.hour-8)
                        #         elif r_e.hour == 15 and instance.created_date.weekday() in [0,1,2,6]:
                        #                 instance.response_time_end_date = r_e + datetime.timedelta(days=1, hours=8)
                        #         elif r_e.hour >15 and instance.created_date.weekday() == 3:
                        #                 instance.response_time_end_date = r_e + datetime.timedelta(days=3, hours=r_e.hour-8)
                        #         elif r_e.hour == 15 and instance.created_date.weekday()==3:
                        #                 instance.response_time_end_date = r_e + datetime.timedelta(days=3, hours=8)
                                

                        instance.save(update_fields=['response_time_end_date', 'response_time_tail_end_date', 'down_time_end_date'])
                machine_calls = instance.machine.calls.exclude(notification_number=instance.notification_number)
                if machine_calls.count() > 0:
                        for call in machine_calls:
                                if instance.created_date and call.created_date:

                                        if instance.created_date.date() < call.created_date.date() + datetime.timedelta(days=instance.machine.machine_callback_time):
                                                instance.callback_call = True
                                                instance.save(update_fields=['callback_call'])

                if instance.customer == None:
                        instance.customer = instance.machine.customer
                        instance.save(update_fields=['customer'])
                
                if instance.engineer:

                        instance.is_assigned=True
                        # call = kwargs.get('instance')
                        instance.status='dispatched'
                        instance.assigned_date = instance.created_date
                        print(instance.assigned_date.weekday())
                        assigned_date_only = instance.assigned_date.date()
                        assigned_time_real = datetime.time(8,0)
                        result_date = datetime.datetime.combine(assigned_date_only, assigned_time_real)
                        send_push_message(instance.engineer.user.ntoken, 'you got new call')

                        if instance.assigned_date.weekday() in [0, 1, 2, 3, 6]:
                                if instance.machine.customer.first_week_dayoff in [7,4,5] and instance.machine.customer.second_week_dayoff in [7,4,5]:
                                        instance.real_assigned_date = instance.assigned_date
                                elif (instance.assigned_date.weekday() == instance.machine.customer.first_week_dayoff and instance.machine.customer.second_week_dayoff != instance.customer.first_week_dayoff + 1) or (instance.assigned_date.weekday() == instance.customer.second_week_dayoff and instance.customer.first_week_dayoff != instance.customer.second_week_dayoff + 1):
                                        instance.real_assigned_date = instance.assigned_date + datetime.timedelta(days=1)
                                elif (instance.assigned_date.weekday() == instance.machine.customer.first_week_dayoff and instance.machine.customer.second_week_dayoff == instance.customer.first_week_dayoff + 1) or (instance.assigned_date.weekday() == instance.customer.second_week_dayoff and instance.customer.first_week_dayoff == instance.customer.second_week_dayoff + 1):
                                        instance.real_assigned_date = instance.assigned_date + datetime.timedelta(days=1)
                                else:
                                        instance.real_assigned_date = instance.assigned_date                                        
                        elif instance.assigned_date.weekday() == 4:
                                
                                if instance.machine.customer.first_week_dayoff in [7,1,2,3,0,4,5] and instance.machine.customer.second_week_dayoff in [7,1,2,3,0,4,5]:

                                        instance.real_assigned_date = result_date + datetime.timedelta(days=2)
                                elif instance.customer.first_week_dayoff == 6 and instance.machine.customer.second_week_dayoff == 0:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=2)                                
                                else:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=2)
                        elif instance.assigned_date.weekday() == 5:
                                if instance.machine.customer.first_week_dayoff in [7,1,2,3,0,4,5] and instance.machine.customer.second_week_dayoff in [7,1,2,3,0,4,5]:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=1)
                                        # print('route1', instance.machine.customer.first_week_dayoff, instance.machine.customer.second_week_dayoff)
                                elif instance.machine.customer.first_week_dayoff == 6 and instance.machine.customer.second_week_dayoff == 0:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=1)                                
                                
                                else:
                                        instance.real_assigned_date = result_date + datetime.timedelta(days=1)
                                        print('route2')
                        else:
                                instance.real_assigned_date = instance.assigned_date


                        # elif instance.assigned_date.weekday()!= 4 and instance.assigned_date.weekday() !=5 and instance.customer.first_week_dayoff
                       



                        instance.previous_status = instance.status
                        engineer = instance.engineer
                        
                        # engineer.no_of_calls += 1
                        # engineer.no_of_calls_dispatched += 1
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
                instance.skip_signal = True
                if instance.created_date == None and instance.assigned_date:
                        instance.created_date = instance.assigned_date
                elif instance.created_date == None and instance.assigned_date == None:
                        instance.created_date = datetime.datetime.now(tz=utc)
                instance.save(update_fields=['created_date'])
                if instance.created_date.weekday() in [0,1,2,3,6] and instance.created_date.hour < 16 and instance.created_date.hour > 7:
                        pass
                        #print('1', instance.created_date.hour, '1111')
                elif instance.created_date.weekday() in [0,1,2,6] and instance.created_date.hour > 15:
                        instance.created_date = datetime.datetime.combine(instance.created_date.date() + datetime.timedelta(days=1), datetime.time(8,0)) 
                        print('2')

                        
                elif instance.created_date.weekday() in [0,1,2,3,6] and instance.created_date.hour < 8:
                        instance.created_date = datetime.datetime.combine(instance.created_date.date(), datetime.time(8,0)) 
                        print('2')                       
                elif instance.created_date.weekday()==3 and instance.created_date.hour > 15:
                        instance.created_date = datetime.datetime.combine(instance.created_date.date() + datetime.timedelta(days=3), datetime.time(8,0))
                        print('3')
                else:
                        print('else', instance.created_date.weekday())
                        if instance.created_date.weekday()==4:
                                time = datetime.time(8,0)
                                date = instance.created_date.date() + datetime.timedelta(days=2)
                                instance.created_date = datetime.datetime.combine(date, time)
                                        
                                                
                        elif instance.created_date.weekday()==5:
                                time = datetime.time(8,0)
                                date = instance.created_date.date() + datetime.timedelta(days=1)
                                instance.created_date = datetime.datetime.combine(date, time)
                                # instance.save(update_fields=['created_date'])
                instance.save(update_fields=['created_date'])
                if instance.created_date:
                        instance.response_time_end_date = egy.localize(instance.created_date) + businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=instance.machine.machine_response_time)
                        print(instance.created_date.replace(tzinfo=utc),businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=instance.machine.machine_response_time))
                        instance.response_time_tail_end_date = egy.localize(instance.created_date) + businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=instance.machine.machine_response_time*1.5)
                        instance.down_time_end_date = egy.localize(instance.created_date) + businesstimedelta.BusinessTimeDelta(working_days_hrs, hours=12)
                        instance.save(update_fields=['response_time_end_date', 'response_time_tail_end_date', 'down_time_end_date'])
 

                        
                machine_calls = instance.machine.calls.exclude(notification_number=instance.notification_number)
                if machine_calls.count() > 0:
                        for call in machine_calls:
                                if instance.created_date and call.real_completed_date:

                                        if instance.created_date.date() < call.real_completed_date.date() + datetime.timedelta(days=instance.machine.machine_callback_time):
                                                instance.callback_call = True
                                                instance.save(update_fields=['callback_call'])

                if instance.customer == None:
                        instance.customer = instance.machine.customer
                        instance.save(update_fields=['customer'])
                
                if instance.created_date and instance.start_of_call:
                        print(instance.created_date.is_naive())
                        pre_response_time = instance.start_of_call - instance.created_date
                        pre_response_time_minutes = pre_response_time / datetime.timedelta(minutes=1)
                        print('a', pre_response_time, pre_response_time_minutes)
                        # instance.response_time = pre_response_time
                        response_time_diff_wh = working_days_hrs.difference(instance.created_date.replace(tzinfo=utc), instance.start_of_call.replace(tzinfo=utc))
                        instance.response_time = datetime.timedelta(hours=response_time_diff_wh.hours, seconds=response_time_diff_wh.seconds)
                        instance.skip_signal=True

                        instance.save(update_fields=['response_time'])
                        # instance.response_time = instance.created_date - instance.start_of_call
                if instance.created_date and instance.real_completed_date:
                        pre_down_time = instance.real_completed_date - instance.created_date
                        pre_down_time_minutes = pre_down_time / datetime.timedelta(minutes=1)
                        print('b', pre_down_time, pre_down_time_minutes)
                        down_time_diff_wh = working_days_hrs.difference(instance.created_date.replace(tzinfo=utc), instance.real_completed_date.replace(tzinfo=utc))
                        instance.down_time = datetime.timedelta(hours=down_time_diff_wh.hours, seconds=down_time_diff_wh.seconds)
                        instance.skip_signal=True
                        # instance.down_time = pre_down_time
                        instance.save(update_fields=['down_time'])
                if instance.down_time:
                        if pre_down_time_minutes < 720:
                                instance.down_success_call = True
                                instance.save(update_fields=['down_success_call'])

                if instance.status == 'completed' and instance.previous_status!='completed':
                        if instance.engineer and instance.previous_status=='incomplete':
                                #engineer = instance.engineer
                                #engineer.no_of_calls_pending -= 1
                                #engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched

                                # engineer.no_ofcalls_success +=1
                                #engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success'])
                                # instance.engineer = engineer
                                instance.previous_status = instance.status
                                instance.completed_date = datetime.datetime.now()
                                instance.save(update_fields=['engineer', 'previous_status', 'completed_date'])
                        elif instance.engineer and instance.previous_status=='dispatched':
                                #engineer = instance.engineer
                                #engineer.no_of_calls_dispatched -= 1
                                #engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - - engineer.no_of_calls_dispatched

                                # engineer.no_ofcalls_success +=1
                                #engineer.save(update_fields=['no_of_calls_dispatched', 'no_ofcalls_success'])
                                # instance.engineer = engineer
                                instance.previous_status = instance.status
                                instance.completed_date = datetime.datetime.now()
                                instance.save(update_fields=['engineer', 'previous_status', 'completed_date'])
                elif instance.status == 'dispatched' and instance.previous_status!='dispatched':
                        if instance.previous_status=='unassigned':
                                print('iam here1')
                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        print('iam here2')
                                        #engineer = instance.engineer
                                        #engineer.no_of_calls += 1
                                        #engineer.no_of_calls_dispatched += 1
                                        #engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending-engineer.no_of_calls_dispatched

                                        #engineer.save(update_fields=['no_of_calls_dispatched', 'no_of_calls', 'no_ofcalls_success'])
                                        instance.previous_status = instance.status
                                        instance.is_assigned = True
                                        now = datetime.datetime.now()
                                        if now.weekday() in [0,1,2,3,6] and now.hour<16 and now.hour > 7:
                                                instance.assigned_date = datetime.datetime.now()
                                        
                                        elif now.weekday() in [0,1,2,3,6] and now.hour < 8:
                                                
                                                r_a = now  + datetime.timedelta(days=1)
                                                rr_a = r_a.date()
                                                instance.assigned_date = datetime.datetime.combine(rr_a, datetime.time(8,0))

                                        elif now.weekday() in [1,2,3,4,6] and now.hour > 15:
                                                if now.weekday() in [0,1,2,6] and now.hour > 15:
                                                        r_a = now  + datetime.timedelta(days=1)
                                                        rr_a = r_a.date()
                                                        instance.assigned_date = datetime.datetime.combine(rr_a, datetime.time(8,0))
                                                
                                                elif now.weekday() == 3 and now.hour > 15:
                                                        r_a = now  + datetime.timedelta(days=3)
                                                        rr_a = r_a.date()
                                                        instance.assigned_date = datetime.datetime.combine(rr_a, datetime.time(8,0))

                                        elif now.weekday() in [4,5]:
                                                if now.weekday() == 4:
                                                        r_a = now + datetime.timedelta(days=2)
                                                        rr_a = r_a.date()
                                                        instance.assigned_date = datetime.datetime.combine(rr_a, datetime.time(8,0))
                                        
                                                        # instance.assigned_date = datetime.datetime.now()
                                                elif now.weekday()==5:
                                                        r_a = now  + datetime.timedelta(days=1)
                                                        rr_a = r_a.date()
                                                        instance.assigned_date = datetime.datetime.combine(rr_a, datetime.time(8,0))
                                        


                                        instance.save(update_fields=['engineer', 'is_assigned', 'previous_status', 'assigned_date'])

                elif instance.status == 'dispatched' and instance.previous_status=='dispatched':
                        print('newhererrreerr')
                        if instance.engineer != instance.previous_engineer:
                                #previous_engineer = instance.previous_engineer
                                # previous_engineer.no_of_calls -= 1
                                # previous_engineer.no_of_calls_dispatched -=1
                                # previous_engineer.save(update_fields=['no_of_calls', 'no_of_calls_dispatched'])
                                engineer = instance.engineer
                                #engineer.no_of_calls +=1
                                #engineer.no_of_calls_dispatched += 1
                                #engineer.save(update_fields=['no_of_calls', 'no_of_calls_dispatched'])
                                instance.previous_engineer = engineer
                                # instance.assigned_date = datetime.datetime.now()
                                instance.save(update_fields=['previous_engineer'])
                elif instance.status == 'unassigned':
                        if instance.previous_status != 'unassigned':
                                if instance.is_assigned == True:
                                        if instance.engineer and instance.engineer!='no engineer assigned yet':
                                                # engineer = instance.engineer
                                                
                                                # engineer.no_of_calls -= 1

                                                # if instance.previous_status == 'dispatched':
                                                #         engineer.no_of_calls_dispatched -= 1
                                                #         engineer.no_of_calls_pending = engineer.no_of_calls_pending
                                                #         engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched

                                                # elif instance.previous_status == 'incomplete':
                                                
                                                #         engineer.no_of_calls_pending -= 1

                                                #         engineer.no_of_calls_dispatched = engineer.no_of_calls_dispatched
                                                #         engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched

                                                # engineer.save(update_fields=['no_of_calls_pending', 'no_of_calls', 'no_ofcalls_success', 'no_of_calls_dispatched'])
                                                instance.engineer = None
                                                instance.assigned_date = None
                                                instance.previous_status = instance.status
                                                instance.is_assigned = False
                                                instance.save(update_fields=['engineer', 'is_assigned', 'previous_status', 'assigned_date'])
                        else:

                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        print('iam hereeeeee')
                                        engineer = instance.engineer
                                        # engineer.no_of_calls += 1
                                        # engineer.no_of_calls_dispatched += 1

                                        # engineer.save(update_fields=['no_of_calls', 'no_of_calls_dispatched'])
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
                                        # if instance.previous_status:
                                        #         if instance.previous_status == 'dispatched':
                                                        
                                        #                 #engineer.no_of_calls +=1
                                        #                 engineer.no_of_calls_pending += 1
                                        #                 engineer.no_of_calls_dispatched -= 1
                                        #                 engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched
                                        #                 engineer.save(update_fields=['no_of_calls_pending','no_of_calls_dispatched', 'no_ofcalls_success','no_of_calls'])
                                                                        
                                
                                        #         # engineer.no_of_calls +=1
                                        #         # engineer.no_of_calls_pending += 1
                                        #         # engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending
                                        #         # engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success','no_of_calls'])
                                        # else:
                                        #         engineer.no_of_calls_pending += 1
                                        #         engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending - engineer.no_of_calls_dispatched
                                        #         engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success'])
                                        #instance.engineer = engineer
                                        instance.previous_status = instance.status
                                        instance.save(update_fields=['engineer', 'previous_status'])
                                else:
                                        # engineer = instance.engineer
                                        # engineer.no_of_calls +=1
                                        # engineer.no_of_calls_pending += 1
                                        # engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending
                                        # engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success', 'no_of_calls'])
                                        instance.engineer = engineer
                                        instance.previous_status = instance.status
                                        instance.save(update_fields=['engineer', 'previous_state'])
 

                                        
                        else:
                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        # engineer = instance.engineer
                                        # engineer.no_of_calls +=1
                                        # engineer.no_of_calls_pending += 1
                                        # engineer.save(update_fields=['no_of_calls_pending', 'no_of_calls'])
                                        # instance.engineer = engineer
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

@receiver(post_save, sender=Report)
def handle_report_save(sender,instance, created,**kwargs):
        if created:
                instance.call.no_of_visits +=1
                instance.call.status = instance.status
                instance.call.save(update_fields=['no_of_visits', 'status'])
                print(instance.starts_at.utcoffset().total_seconds())
                if instance.starts_at.replace(tzinfo=utc) < instance.call.response_time_end_date.replace(tzinfo=utc) and instance.no_of_visits==1:
                        instance.call.response_success_call = True
                        instance.call.save(update_fields=['response_success_call'])
                if instance.call.reports.count()==1:
                        if instance.status == 'completed':
                                instance.call.first_time_finish = True
                                instance.call.start_of_call = instance.starts_at.replace(tzinfo=utc)
                                instance.call.real_completed_date = instance.finishs_at.replace(tzinfo=utc)
                                instance.call.save(update_fields=['first_time_finish', 'start_of_call', 'real_completed_date'])
                        elif instance.status =='incomplete':
                                instance.call.start_of_call = instance.starts_at
                                instance.call.save(update_fields=['start_of_call'])
                
                elif instance.call.reports.count() > 1:
                        if instance.status == 'completed':
                                # instance.call.first_time_finish = True
                                # instance.call.start_of_call = instance.starts_at
                                instance.call.real_completed_date = instance.finishs_at
                                instance.call.save(update_fields=['real_completed_date'])
                        elif instance.status =='incomplete':
                                instance.call.delayed_call = True
                                instance.call.save(update_fields=['delayed_call'])
                send_push_message(instance.engineer.user.ntoken, 'engineer {} has created a report for {}'.format(instance.call.engineer.name, instance.call.notification_number))

        else:
                pass