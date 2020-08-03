import random
from .models import Machine as ma
from machine.models import Machine

def advertisments(request):
    pass
    count = Machine.objects.filter(customer__name='mai').count()
    mas= Machine.objects.filter(customer__name='mai').all()
    return {'ma':mas[random.randrange(0,count)]}
    
    