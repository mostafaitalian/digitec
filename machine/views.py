from django.shortcuts import render, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import Machine, Call, Category, Report, Contract
from .forms import CreateMachineForm, CallForm, CategoryForm, ReportForm,ReportForm2, ReportForm1, CallFormSet,CallForm1, CallForm2, MachineForm, ContractForm, ReportFormSet
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from engineer.models import Engineer, Area
from customer.bulk_machines import create_bulk
from customer.models import Department, Customer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import MachineSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib import messages
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView 
# Create your views here.
import json
from django.conf import settings
from django.core.mail import send_mail



class CreateMachineView1(CreateView):
    model = Machine
    form_class = CreateMachineForm
    template_name = "machine/create_machine2.html"
    success_url = reverse_lazy('customer:customer-list')
    def get(self, request):
        # customer = customer_slug
        
        customer_s = request.GET.get('id', None)
        if customer_s:
            customer_instance = Customer.objects.get(pk=customer_s)
            form = self.form_class(initial={'customer':Customer.objects.get(pk=customer_s), 'area':customer_instance.area, 'engineers': Engineer.objects.filter(area=customer_instance.area)})
            form.fields['department'].queryset = Department.objects.filter(customer__id=customer_s)
            
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form':form})

class CreateMachineView(CreateView):
    model = Machine
    form_class = CreateMachineForm
    template_name = "machine/create_machine.html"
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            customer = form.save(request)
            return redirect(customer)
        else:
            return render(request, self.template_name,{'form':form})
    
class MachineList(LoginRequiredMixin,ListView):
    model = Machine
    template_name = "machine/machine_list.html"
    context_object_name = 'machine_list'
    paginate_by=8
    def get_queryset(self):
        # ctx = super().get_context_data(**kwargs)
        # ctx['all_machines'] = Machine.objects.all()
        # return ctx
        if self.request.user.is_superuser:
            q=Machine.objects.all()
        else:
            q=None
        return q

        
    #         ctx['all_machines'] = all_machines
    #         return ctx
            
    #     # elif self.request.user.is_authenticated and hasattr(self.request.user, 'engineer'):
    #     #     all_machines = Machine.objects.filter(area=self.request.user.engineer.area)
    #     else:
    #         all_machines = None
    #         ctx['all_machines'] = all_machines
    #         return ctx
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["machiness"] =Machine.objects.all() 
        return context
    
class MachineCreateReadView(ListCreateAPIView):
    # queryset=Machine.objects.all()
    serializer_class = MachineSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Machine.objects.all()
        elif self.request.user.engineer:
            return Machine.objects.filter(engineers__in=[self.request.user.engineer.id])
        else:
            return None
    # authentication_classes=(SessionAuthentication, BaseAuthentication, JSONWebTokenAuthentication)
    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return Machine.objects.all()
    #     return Machine.objects.filter(engineers__in=[self.request.user.engineer.id,])
# class MachineDetailUpdateView(RetrieveUpdateDestroyAPIView):
#     queryset = Machine.objects.all()
#     serializer_class = MachineSerializer


class MachineUpdateReadView(RetrieveUpdateDestroyAPIView):
    queryset=Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'slug'
class CallCreateView(CreateView):
    template_name="machine/create_call.html"
    model = Call
    form_class = CallForm
    success_url = reverse_lazy("machine:call_create")
    def get_context_data(self, *args,**kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        return ctx
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request':self.request})
        return kwargs
    # def get_context_data(self, *args,**kwargs):
    #     ctx = super().get_context_data(*args, **kwargs)
    #     return ctx

class MachineDetailView(DetailView):
    template_name = 'machine/machine_detail.html'
    model = Machine
    context_object_name = 'machine' 
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['calls']=Call.objects.filter(machine__id=self.object.id)
        return ctx

class CallDetailView(DetailView):
    template_name = 'machine/call_detail.html'
    model = Call
    context_object_name = 'calll' 
    def get_object(self, **kwargs):
        call = Call.objects.get(pk=int(self.kwargs['pk']))
        print(call.notification_number)
        if self.request.user.is_superuser or self.request.user.engineer:
            
            print(kwargs)
            return call
        elif self.request.user.is_authenticated and hasattr(call.engineer, 'user'):
                if self.request.user == call.engineer.user:
                    return call
        else:

            return call
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ReportForm1()
        ctx['assign_form'] = CallForm2()
        return ctx


class CallListView(ListView):

    model = Call
    template_name = "machine/call_list.html"
    context_object_name = 'call_list'
    # paginate_by=5
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Call.objects.all()

        elif self.request.user.is_active:
            return Call.objects.filter(engineer__user=self.request.user)
        else:
            return None

class CreateCategory(CreateView):
    template_name='machine/create_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("machine:create_category")


class MachineOfCustomerListApi(ListCreateAPIView):
    serializer_class=MachineSerializer
    
    # def get_serializer(self, instance=None, data=None, many=False, partial=False):
        # if isinstance(data, list):
        #     return super().get_serializer(self, instance=instance, data=data, many=True, partial=partial)
        # else:
        #     return  super().get_serializer(self, instance=instance, data=data, many=False, partial=partial)
    def get_queryset(self):
        return Machine.objects1.get_machines_by_customer(self.kwargs.get('customer_id'))
    

class ReportCreate(CreateView):
    model = Report
    form_class = ReportForm1
    template_name = 'machine/create_report.html'
    success_url = reverse_lazy("machine:call_list",)

    def form_valid(self, form):
        status = form.cleaned_data['status']
        print(status)
        call = form.cleaned_data['call']
        call.status = status
        
        call_instance =Call.objects.get(pk=call.notification_number)
        call_instance.status= status
        print(call_instance.status)

        call_instance.save()
        # print(call_instance.status)

        # form.cleaned_data['call'] = call_instance
        print(form.cleaned_data['call'].status)
        print(call.status, form.cleaned_data['call'].status)
        form.save()
        print(call.status)


        # report.save(force_update=True)
        # print(report.call.status)
        # form.save()
        # return redirect('machine:report_list')
        return super().form_valid((form))

class ReportList(ListView):
    model=Report
    template_name='machine/report_list.html'
    queryset = Report.objects.all()
    context_object_name='reports'
def create_report(request,pk):
    if request.method=='POST':
        form = ReportForm1(request.POST)
        
        if form.is_valid():
            
            form.save()
            return redirect('machine:report_list')
        else:
            return render(request, 'machine/create_report.html',{'form':ReportForm1(initial=request.POST),'req':request.POST})
        
        
        return redirect('machine:call_detail', pk)

class MachineListCustom(ListView):
    model=Machine
    template_name='machine/machine-list-custom.html'
    context_object_name='machines'
    paginate_by=4
    def get_queryset(self):
        query=self.request.GET.get('query','')
    

        if self.request.GET.get('category','') == 'name':
            machines = Machine.objects.filter(name__icontains=query)
            total_page = machines.count()/self.paginate_by


            return machines
        elif self.request.GET.get('category', '') == 'serial':
            machines = Machine.objects.filter(serial__icontains=query)
            return machines
        elif self.request.GET.get('category','') == 'customer':
            machines = Machine.objects.filter(customer__name__icontains=query)
            return machines
        else:
            return super().get_queryset()
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('query', '')
        ctx['category'] = self.request.GET.get('category','')
        return ctx   

def create_bulk_machines(request):
    machines = []
    for i in range((0,999)):
        machine = Machine(name='7845',serial=11111111+i, )

        pass
def create_update_call_formset(request, notification=None):
    serial = request.GET.get('serial', None)
    print(serial)
    if serial:
        print(serial)
        try:
            machine = Machine.objects.get(serial__icontains=serial)
            
        except:
            messages.warning(request, 'No machine found with this serial')
            return redirect('machine:call_manage')
        # machine = get_object_or_404(Machine, serial__icontains=serial)

        print(machine.serial)
        call=Call(customer=machine.customer, machine=machine)
        # call.save(commit=False)
        print('{}{}'.format(machine.serial, serial))
        
    
    else:
        if notification:
            call =  Call.objects.get(notification_number=notification)
        else:
            call = Call()

    call_form = CallForm1(instance=call)
    formset = CallFormSet(instance=call)
    if request.method =='POST':
        created_call_form = CallForm1(request.POST, instance=call)
        if notification:
            created_call_form = CallForm1(request.POST, instance=call)
        # created_call_form = call_form.save(commit=False)
        created_formset = CallFormSet(request.POST, request.FILES, instance=call)
        if created_call_form.is_valid():
            print('inside POst valid')
            created_call= created_call_form.save()
            if created_formset.is_valid():

                # created_call.save()
                created_formset.save()

                return redirect(reverse('machine:call_list'))
    print('{}---{}'.format(call.notification_number, call.created_date))
    return render(request, 'machine/manage_call.html', {'call_form':call_form, 'formset':formset, 'notification_number': call.notification_number})


class CallUpdateView(UpdateView):
    model=Call
    form_class=CallForm2
    template_name='machine/call_assign_engineer.html'
    def get_success_url(self):
        return reverse('machine:call_detail', kwargs={'pk':self.object.notification_number})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assign_form"] = self.get_form()
        return context
    def form_valid(self, form):
        engineer = form.cleaned_data['engineer']
        form.save()
        
        s = 'you got a new call {}'.format(self.object.notification_number) 
        m = 'you got a new call with notification number {} its assigned date {} you have {} to respond to machine'.format(self.object.notification_number,
        self.object.assigned_date, self.object.machine.machine_response_time)
        
        send_mail(subject=s, message=m, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['myossef@digitecxerox.com'],)

        return super().form_valid(form)















def create_update_machine(request, serial_number=None):
    serial = request.GET.get('serial', None)
    print(serial)
    if serial_number:
        print(serial_number)
        try:
            machine = Machine.objects.get(serial__icontains=serial_number)
            if machine.contract:
                contract = machine.contract
            else:
                contract=Contract()
            
        except:
            messages.warning(request, 'No machine found with this serial')
            return redirect('machine:machine_manage')
        # machine = get_object_or_404(Machine, serial__icontains=serial)

        # print(machine.serial)
        # call=Call(customer=machine.customer, machine=machine)
        # # call.save(commit=False)
        # print('{}{}'.format(machine.serial, serial))
        
    elif serial:
        try:
            machine = Machine.objects.get(serial__icontains=serial)
            if machine.contract:
                contract = machine.contract
            else:
                contract=Contract()
        except:
            messages.warning(request, 'No machine found with this serial')
            return redirect('machine:machine_manage')
    else:
            machine= Machine()
            contract=Contract()

    machine_form = MachineForm(instance=machine)
    contract_form = ContractForm(instance=contract)
    if request.method =='POST':
        created_machine_form = MachineForm(request.POST, instance=machine)

        # created_call_form = call_form.save(commit=False)
        created_contract_form = ContractForm(request.POST, request.FILES, instance=contract)
        if created_machine_form.is_valid() and created_contract_form.is_valid():
            print('inside POst valid')
            created_machine= created_machine_form.save(commit=False)
            
            created_contract = created_contract_form.save()
            created_machine.contract = created_contract
            created_machine.save()



            return redirect(reverse('machine:machine_detail', kwargs={'pk':created_machine.id}))
    # print('{}---{}'.format(call.notification_number, call.created_date))
    return render(request, 'machine/manage_machine.html', {'machine_form':machine_form, 'contract_form':contract_form, 'serial_number': machine.serial})


def bulk(request):
    customers = Customer.objects.all()
    data_list = create_bulk(customers)
    da = json.loads(json.dumps(data_list,indent=4, ensure_ascii=False).encode('utf-8'))
    print(da)
    daa = [item['fields'] for item in da]
    print(json.loads(json.dumps(daa)))
    for d in daa:
        customer = Customer.objects.get(id=d['customer'])
        d['customer']=customer
        area = Area.objects.get(id=d['area'])
        d['area'] = area
        department = Department.objects.get(id=d['department'])
        d['department'] = department
    Machine.objects.bulk_create([Machine(**i) for i in daa])
    return redirect('machine:list')


class ReportList(LoginRequiredMixin, ListView):
    model = Report
    template_name='machine/report-list.html'
    context_object_name = 'reports'
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            query=self.request.GET.get('query','')
            print(self.request.GET.get('query'), self.request.GET.get('categoryy'))

            if self.request.GET.get('categoryy','') == 'notification_number':
                reports = Report.objects.filter(call__notification_number=query)
                # total_page = machines.count()/self.paginate_by


                return reports
            elif self.request.GET.get('categoryy', '') == 'serial':
                reports = Report.objects.filter(call__machine__serial=query)
                return reports
            elif self.request.GET.get('categoryy','') == 'customer':

                reports = Report.objects.filter(call__customer__name__icontains=query)
                return reports
            elif self.request.GET.get('categoryy','') == 'engineer':
                
                reports = Report.objects.filter(call__engineer__name__icontains=query)
                return reports
            else:
                return super().get_queryset()
            if self.request.user.is_superuser:
                q = self.model.objects.all()
            elif hasattr(self.request.user, 'engineer'):
                q = self.model.objects.filter(engineer=self.request.user.engineer)
        else:
            q= None
        return q                
def create_update_report_formset(request, id=None):
    if id:
        report = Report.objects.get(id=id)
    else:
        report = Report()
    report_form = ReportForm1(instance=report)
    formset = ReportFormSet(instance=report)
    if request.method =='POST':
        if id:
            created_report_form = ReportForm2(request.POST,request.FILES, instance=report)
        else:
            created_report_form = ReportForm1(request.POST,request.FILES, instance=report)

        # created_call_form = call_form.save(commit=False)
        created_formset = ReportFormSet(request.POST, request.FILES, instance=report)
        if created_report_form.is_valid():
            print('inside POst valid')
            created_report= created_report_form.save()
            if created_formset.is_valid():

                # created_call.save()
                created_formset.save()

                return redirect(reverse('machine:report_list'))
    # print('{}---{}'.format(call.notification_number, call.created_date))
    if id:
        return render(request, 'machine/manage_report.html', {'report_form':ReportForm2(instance=report), 'formset':formset, 'id':id}) 
    return render(request, 'machine/manage_report.html', {'report_form':report_form, 'formset':formset, 'id':id})
