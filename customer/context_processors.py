import random
from .models import Customer as cu
from machine.models import Machine

def advertisments(request):
    count = Machine.objects.filter(customer__name='mai').count()
    mas= Machine.objects.filter(customer__name='mai').all()
    return {'ma':mas[random.randrange(0,count)]}
def customer_adv(request):
    count=cu.objects.all().count()
    cus = cu.objects.all()
    return {'cu':cus[random.randrange(0,count)]}