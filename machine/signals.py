from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Call, Machine
from customer.models import Department

@receiver(post_save, sender=Machine)
def handle_machine_save(sender, instance, created, **kwargs):
        if created:

                department = Department.objects.get(pk=instance.department.id)
                department.no_of_machine +=1

                department.save(update_fields=['no_of_machine'])
                instance.department = department

previous_state = ""
@receiver(post_save, sender=Call)
def handle_call_save(sender,instance,created, **kwargs):
        
        if created:
                if instance.engineer:

                        instance.is_assigned=True
                        # call = kwargs.get('instance')
                        instance.status='pending'
                        # instance.previous_status = instance.status
                        engineer = instance.engineer
                        engineer.no_of_calls += 1
                        engineer.no_of_calls_pending += 1
                        engineer.save()
                        instance.engineer = engineer
                        instance.previous_status = instance.status
    
                        # print(instance.status)
                        instance.save()
                        return
                else:
                        instance.previous_status = 'unassigned'
                        instance.save()
                        return

        else:

                if instance.status == 'completed' and instance.previous_status!='completed':
                        if instance.engineer:
                                engineer = instance.engineer
                                engineer.no_of_calls_pending -= 1
                                engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending

                                # engineer.no_ofcalls_success +=1
                                engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success'])
                                instance.engineer = engineer
                                instance.previous_status = instance.status
                                instance.save(update_fields=['engineer', 'previous_status'])
                elif instance.status == 'unassigned':
                        if instance.previous_status != 'unassigned':
                                if instance.is_assigned == True:
                                        if instance.engineer and instance.engineer!='no engineer assigned yet':
                                                engineer = instance.engineer
                                                engineer.no_of_calls -= 1
                                                engineer.no_of_calls_pending -= 1
                                                engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending

                                                engineer.save(update_fields=['no_of_calls_pending', 'no_of_calls', 'no_ofcalls_success'])
                                                instance.engineer = None
                                                instance.previous_status = instance.status
                                                instance.is_assigned = False
                                                instance.save(update_fields=['engineer', 'is_assigned', 'previous_state'])
                        else:

                                if instance.engineer and instance.engineer!='no engineer assigned yet':
                                        print('iam hereeeeee')
                                        engineer = instance.engineer
                                        engineer.no_of_calls += 1
                                        engineer.no_of_calls_pending += 1
                                        engineer.save(update_fields=['no_of_calls', 'no_of_calls_pending'])
                                        instance.is_assigned=True
                                        instance.status='pending'
                                        instance.save(update_fields=['engineer', 'is_assigned', 'status'])



                elif instance.status =='pending' and instance.previous_status != 'pending':
                        if instance.is_assigned == True:
                                if instance.engineer and instance.engineer != 'no engineer assigned yet':
                                        engineer = instance.engineer
                                        if instance.previous_status:
                                                pass
                                                # engineer.no_of_calls +=1
                                                # engineer.no_of_calls_pending += 1
                                                # engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending
                                                # engineer.save(update_fields=['no_of_calls_pending', 'no_ofcalls_success','no_of_calls'])
                                        else:
                                                engineer.no_of_calls_pending += 1
                                                engineer.no_ofcalls_success = engineer.no_of_calls - engineer.no_of_calls_pending
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
                                        instance.save(update_fields=['engineer'])
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
