from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
# from .models import Call, Machine, Contract
from .models import Department, Customer
import datetime
from django.utils import timezone
from django.db import transaction
from dateutil.relativedelta import relativedelta



@receiver(post_save, sender=Customer)
def handle_customer_save(sender, instance, created, **kwargs):
    print('11111111')
    if created:
        print('customer create signal')
        department = Department(department_name='others', customer=instance)
        department.save()
