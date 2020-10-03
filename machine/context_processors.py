import random
from .models import Machine
from machine.models import Machine
from customer.models import Customer
from django.db.models import Count
def advertisments(request):
    # pass
    
    customers_highest_machines = Customer.objects.all().annotate(customer_machines=Count('machines')).order_by('-customer_machines')[0:3]
    # total_machines = customers_highest_machines.machines.count()
    machines_per_customer = [customer.machines.count()  for customer in customers_highest_machines]
    total_machines  = sum(machines_per_customer)
    return({'customers':customers_highest_machines, 'total_machines': total_machines, 'machines_per_customer': machines_per_customer})
    # machines = Machine.objects.all()
    # customer = Customer.objects.get(name__icontains='gdj')
    # machines2 = machines.filter(id=1)
    # count = Machine.objects.filter(customer__name__icontains='gdj').count()
    # mas= Machine.objects.filter(customer__name__startswith='gdj')
    # exMachine = Machine.objects.get(pk=1).serial
    # return {'ma':machines, 'mas': mas, 'count':total_machines, 'ma2':machines2, 'f':customer_highest_machines}
    # pass
    
    