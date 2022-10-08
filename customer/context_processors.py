import random
from machine.models import Machine

from .models import Customer

def advertisments(request):
    count = Machine.objects.filter(customer__name='mai').count()
    mas= Machine.objects.filter(customer__name='mai').all()
    return {'ma':mas[random.randrange(0,count)]}
def customer_adv(request):
    count=Customer.objects.all().count()
    cus = Customer.objects.all()
    # return {'cu':cus[random.randint(0,count-1)]}
    return {'cu': 1}