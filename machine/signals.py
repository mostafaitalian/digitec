from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Call, Machine
from customer.models import Department
import datetime
from django.utils import timezone




@receiver(post_save, sender=Machine)
def handle_machine_save(sender, instance, created, **kwargs):
        if created:

                department = Department.objects.get(pk=instance.department.id)
                department.no_of_machine +=1

                department.save(update_fields=['no_of_machine'])
                instance.department = department
                if instance.customer:
                        if instance.customer.organization:
                                instance.customer.organization.save(update_fields=['organization_machines_number'])

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
        
        if created:
                if instance.engineer:

                        instance.is_assigned=True
                        # call = kwargs.get('instance')
                        instance.status='dispatched'
                        instance.assigned_date = datetime.datetime.now()
                        # instance.previous_status = instance.status
                        engineer = instance.engineer
                        engineer.no_of_calls += 1
                        engineer.no_of_calls_dispatched += 1
                        # engineer.no_of_calls_pending += 1
                        engineer.save()
                        instance.engineer = engineer
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
                        if instance.engineer and instance.previous_status=='pending':
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
                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        engineer = instance.engineer
                                        engineer.no_of_calls += 1
                                        engineer.no_of_calls_dispatched += 1
                                        engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending-engineer.no_of_calls_dispatched

                                        engineer.save(update_fields=['no_of_calls_dispatched', 'no_of_calls', 'no_ofcalls_success'])
                                        instance.previous_status = instance.status
                                        instance.is_assigned = True
                                        instance.assigned_date = datetime.datetime.now()
                                        instance.save(update_fields=['engineer', 'is_assigned', 'previous_status', 'assigned_date'])


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

                                                elif instance.previous_status == 'pending':
                                                
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
                                        instance.status='dispatched'
                                        instance.previous_status = 'dispatched'
                                        instance.assigned_date = datetime.datetime.now()
                                        instance.save(update_fields=['engineer', 'is_assigned', 'status', 'previous_status', 'assigned_date'])



                elif instance.status =='pending' and instance.previous_status != 'pending':
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
