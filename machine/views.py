import os
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
from .serializers import MachineSerializer, CallSerializer, ReportSerializer, ReportSerializer1
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django.shortcuts import get_object_or_404
from django.contrib import messages
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView 
from .filters import MachineFilter, CallFilter
from rest_framework import status as rest_status 
# Create your views here.
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from dateutil import parser       
# from django.conf import settings
from django.conf import settings
from django.core.mail import send_mail
from PIL import Image




# img = Image()

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
    paginate_by=100
    def get_queryset(self):
        # ctx = super().get_context_data(**kwargs)
        # ctx['all_machines'] = Machine.objects.all()
        # return ctx
        if self.request.user.is_superuser:
            q=Machine.objects.all()
        else:
            q=Machine.objects.all()
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
        if Machine.objects.all().count()>0:
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
            return Machine.objects.filter(area__id=[self.request.user.engineer.area.id])
        else:
            return None
class CallCreateReadView(ListCreateAPIView):
    # queryset=Machine.objects.all()
    serializer_class = CallSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Call.objects.all()
        elif self.request.user.engineer and self.reuest.user.is_superuser:
            return Call.objects.filter(engineer__id=self.request.user.engineer.id)
        elif self.request.user.engineer:
            return Call.objects.filter(engineer__id=self.request.user.engineer.id)

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
class CallCreateReadViewAll(ListCreateAPIView):
    serializer_class = CallSerializer
    # lookup_field = 'slug'
    queryset=Call.objects.all()

    permission_classes = (IsAuthenticated,)
class ReportCreateReadView(ListCreateAPIView):
    # queryset=Machine.objects.all()
    serializer_class = ReportSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Report.objects.all()
        elif self.request.user.engineer:
            return Report.objects.filter(engineer__id=[self.request.user.engineer.id])
        else:
            return None

class MachineUpdateReadView(RetrieveUpdateDestroyAPIView):
    queryset=Machine.objects.all()
    serializer_class = MachineSerializer
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
        
        send_mail(subject=s, message=m, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['myossef@digitecxerox.com', engineer.user.email],)

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



workcentre_black_category_s = [
        'b405','405B', '405b','B405',
        '4150', '4260','4250',
        'M 20', 'M20', 'M 15', 'M15',
        '4118',
        '3550',  '3655', '3635',
        '412', '420', '315',
        'b215', 'B215', '215B', '215b',
        '4510', '4210',
        'B605','B615', '605B', '615B', 'b605', 'b615','605b','605b',
        '5016','5020', '5019', '5021', '5022', '5024',
        '1022B', '1025B', 'b1022', 'b1025','1025', '1022',

]
workcentre_black_category_m = [
        'b7025', 'b7030', 'b7035',
        '7025B', '7030B', '7035B',
        '7025b', '7030b', '7035b',
        '7030',
        '5500',


        '5325', '5330', '5335', '5322',
        '5225', '5230', '5235', '5225A', '5230A', '5235A','5222',
        '128', '133', '118',
]
workcentre_black_category_l = [
        '255', '265', '275', '245', '55', '45',
        '5635', '5645', '5655', '5665','5675', '5690', '6532',
        '5735', '5745', '5755', '5765','5775', '5790',
        'b8045', 'b8055', 'b8065', 'b8075', 'b8090', '8045B', '8055B', '8065B','8075B', '8090B', '8045b', '8055b', '8065b','8075b', '8090b',
        '5945', '5955',
        '5855', '5845', '5865','5875', '5890',
]
workcentre_color_category_s = [
        'c405', '405C','C405',
        '6180',
        'c605', '605C','c615', '615C',
]
workcentre_color_category_m = [
     'c7025', 'c7030', 'c7035','7025C', '7030C', '7035C',

     '7225', '7220', '7230', '7221', '7121',
     '7120', '7125', '7132', '7232','7242',
     '6655',



]
workcentre_color_category_l = [

        '7830','7835', '7845', '7855',
        '7328','7365', '7366',
        '7428',
        '7530', '7535', '7545', '7555', '7560',
        '7990',
        'c8030', 'c8035', 'c8045', 'c8055', 'c8065', 'c8075', '8035C', '8030C', '8045C', '8055C', '8065C',

]
phasor_black_category = ['3615','3310', '3315','3600', '3320', '3330', '3345',
                            '3325','3250', '3260', '3215', '3220', '3225', '3235', '3245', '3230',
                            '3200', '3210', '3335','3020', '3025','3030', '3035','3040', '3045', '3420', '3425', '3430', '3435', '3450',
                            '3610', '3600',
                            'pe220', 'PE220', 'pe16', 'PE16','pe120', 'PE120',
                            ]
phasor_color_category = ['8880', '8870', '6510', '6515']
radiology_category = ['c60', '550', '560','C60', 'C70','60C', 'c70','C70', 'j70','c9065', 'c75', 'C75', '9065C', 'c9065', 'C9065']
production_color_category = ['180', '2100', '3100','280', '4100', 'V180']
production_black_category = ['D95', '9100B', 'b9100', 'B9100', 'b9100', 'D125']
wide_format_category = ['6204', '6705', '510', '6050']
def bulk(request):
    # all customer objects in db
    customers = Customer.objects.all()
    # 
    data_list = create_bulk(customers)
    da = json.loads(json.dumps(data_list,indent=4, ensure_ascii=False).encode('utf-8'))
    print(da)
    daa = [item['fields'] for item in da]
    print(json.loads(json.dumps(daa)))
    new_notexist_machines = []
    update_exist_machines = []
    for d in daa:
        customer = Customer.objects.get(id=d['customer'])
        d['customer']=customer
        area = Area.objects.get(id=d['area'])
        d['area'] = area
        department = Department.objects.get(id=d['department'])
        d['department'] = department
        if d['serial'] in Machine.objects.values_list('serial', flat=True):
            dict_machine = dict(**d)
            dict_machine.pop("added", None)
            if d["added"] == None:
                dict_machine.pop("added", None)

            machine_selected = Machine.objects.filter(serial=d['serial']).update(**dict_machine)
            
            print('44444')

            update_exist_machines.append(machine_selected)
        else:
            new_notexist_machines.append(d)
    # Machine.objects.bulk_update([Machine(**i) for i in update_exist_machines])
    Machine.objects.bulk_create([Machine(**i) for i in new_notexist_machines])
    for machine in Machine.objects.all():
        machine.save(update_fields=['machine_model'])
        
        if machine.machine_model:
                if machine.machine_model in workcentre_black_category_s:
                    print('2')
                    machine.machine_category = 'mono workcentre'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points = 0.8
                    pass
                elif machine.machine_model in workcentre_black_category_m:
                    print('2')
                    machine.machine_category = 'mono workcentre'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points = 1
                    pass
                elif machine.machine_model in workcentre_black_category_l:
                    print('2')
                    machine.machine_category = 'mono workcentre'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points = 1.4
                    pass
                elif machine.machine_model in workcentre_color_category_s:
                    print('3')
                    machine.machine_category = 'color workcentre'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points = 1
                    pass
                elif machine.machine_model in workcentre_color_category_m:
                    print('3')
                    machine.machine_category = 'color workcentre'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points = 1.2
                    pass
                elif machine.machine_model in workcentre_color_category_l:
                    print('3')
                    machine.machine_category = 'color workcentre'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points = 2
                    pass
                elif machine.machine_model in phasor_black_category:
                    print('4')
                    machine.machine_category = 'mono phasor'
                    machine.machine_response_time = 9
                    machine.machine_callback_time = 7
                    machine.machine_points = 0.6
                    pass
                elif machine.machine_model in phasor_color_category:
                    print('5')
                    machine.machine_category = 'color phasor'
                    machine.machine_response_time = 9
                    machine.machine_callback_time = 7
                    machine.machine_points = 0.8
                    pass
                elif machine.machine_model in radiology_category:
                    print('6')
                    machine.machine_category = 'radiology'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points =  2
                    pass
                elif machine.machine_model in production_black_category:
                    print('7')
                    machine.machine_category = 'mono production'
                    machine.machine_response_time = 4
                    machine.machine_callback_time = 4
                    machine.machine_points = 2
                    pass
                elif machine.machine_model in production_color_category:
                    print('8')
                    machine.machine_category = 'color production'
                    machine.machine_response_time = 4
                    machine.machine_callback_time = 4
                    machine.machine_points = 2
                    pass
                elif machine.machine_model in wide_format_category:
                    machine.machine_category = 'wide format'
                    machine.machine_response_time = 6
                    machine.machine_callback_time = 7
                    machine.machine_points =  1.6
                else:
                    print('9')
                    pass

        machine.save()

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
def search_machine(request):
    machines = Machine.objects.all()
    machine_filter = MachineFilter(request.GET, queryset=machines)
    return render(request, 'machine/machine_list_filter.html', {'filter': machine_filter})

def search_call(request):
    calls = Call.objects.all()
    call_filter = CallFilter(request.GET, queryset=calls)
    return render(request, 'machine/call_list_filter.html', {'filter': call_filter})
def call_list_custom_n(request, status=None):
    all_calls = Call.objects.all().order_by('notification_number')
    own_calls = None
    if status==None:
        if hasattr(request.user, 'engineer') and request.user.is_superuser:
            own_calls = Call.objects.filter(engineer=request.user.engineer).order_by('created_date')
            # all_calls = Call.objects.all().order_by('created_date')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif request.user.is_superuser:
            own_calls = None
            # all_calls = Call.objects.all().order_by('created_date')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif hasattr(request.user, 'engineer'):
            own_calls = Call.objects.filter(engineer=request.user.engineer).order_by('created_date')
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        else:
            own_calls = None
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
    elif status=='unassigned':
        if hasattr(request.user, 'engineer') and request.user.is_superuser:
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='unassigned').order_by('created_date')
            all_calls = all_calls.filter(status='unassigned')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif request.user.is_superuser:
            own_calls = None
            all_calls = all_calls.filter(status='unassigned')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif hasattr(request.user, 'engineer'):
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='unassigned').order_by('created_date')
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        else:
            own_calls = None
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
    elif status=='dispatched':
        if hasattr(request.user, 'engineer') and request.user.is_superuser:
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='dispatched').order_by('created_date')
            all_calls = all_calls.filter(status='dispatched')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif request.user.is_superuser:
            own_calls = None
            all_calls = all_calls.filter(status='dispatched')
            # return render(request, 'machine/call_list3_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif hasattr(request.user, 'engineer'):
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='dispatched').order_by('created_date')
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        else:
            own_calls = None
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
    elif status=='incomplete':
        if hasattr(request.user, 'engineer') and request.user.is_superuser:
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='incomplete').order_by('created_date')
            all_calls = all_calls.filter(status='incomplete')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif request.user.is_superuser:
            own_calls = None
            all_calls = all_calls.filter(status='incomplete')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif hasattr(request.user, 'engineer'):
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='incomplete').order_by('created_date')
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        else:
            own_calls = None
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
    elif status=='completed':
        if hasattr(request.user, 'engineer') and request.user.is_superuser:
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='completed').order_by('created_date')
            all_calls = all_calls.filter(status='completed')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif request.user.is_superuser:
            own_calls = None
            all_calls = all_calls.filter(status='completed')
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        elif hasattr(request.user, 'engineer'):
            own_calls = Call.objects.filter(engineer=request.user.engineer).filter(status='completed').order_by('created_date')
            all_calls = None
            # return render(request, 'machine/call_list1_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
        else:
            own_calls = None
            all_calls = None
            # return render(request, 'machine/call1_list_status.html', {'own_calls': own_calls, 'all_calls': all_calls})
    return render(request,
    'machine/call_list3_status.html',
    {'own_calls': own_calls, 'all_calls': all_calls, 'status': status})

class ReportCreate2ApiView(CreateAPIView):
    
    serializer_class = ReportSerializer1
    parser_class= (FileUploadParser,)
    
    def create(self, request, *args, **kwargs):
        #setattr(request.data, '_mutable', True)
        #data = request.data.copy()
        print((request.data['call']))
        print((request.data['starts_at']))
        #print((request.data['finishs_at']))
        call = int((request.data['call']))
        status = ((request.data['status']))
        
        if hasattr(request.data, 'image'):
            image = ((request.data['image']))
        else:
            image = None
        if hasattr(request.data, 'report_copy'):
            report_copy = ((request.data['report_copy']))
        else:
            report_copy = None
        engineer = int((request.data['engineer']))
        starts_at = ((request.data['starts_at']))
        finishs_at = ((request.data['finishs_at']))
        data = {}
        data['call'] = call
        data['engineer'] = engineer
        data['status'] = status
        print(request.data, request)
        print(data)

        #data['starts_at'] = starts_at
        #data['finishs_at'] = finishs_at
        #data['image'] = image
        if image !=None:
            print('1')
            path = default_storage.save('tmp/report.jpeg', ContentFile(image.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            print('path',tmp_file)
            data['image'] = image
        elif report_copy !=None:
            print('2')
            path = default_storage.save('tmp/file.pdf', ContentFile(report_copy.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            print('path',tmp_file)
            data['report_copy'] = report_copy
        #print(image.name)


        call_instance = Call.objects.get(notification_number=call)
        engineer_instance = Engineer.objects.get(id=engineer)

        report =Report(call=call_instance, engineer=engineer_instance,
        status=status, image=image,starts_at=parser.parse(starts_at),
        finishs_at=parser.parse(finishs_at))
        if report:    
            report.save()
            return Response({'report': 'created'},status=rest_status.HTTP_201_CREATED)
        return Response({'report': 'Not created'},status=rest_status.HTTP_404_NOT_FOUND)
        #report = ReportSerializer1(data=data)
        #print(report.is_valid())
        #if report.is_valid():
        #    report.save()
        #    report.image = image
        #    report.save(update_fields=['image'])
        # return Response({'report': 'created'},status=rest_status.HTTP_201_CREATED)
        #return Response(data)
        #print(report.errors)
        #return super().create(request, *args, **kwargs)
        #formData.append('finishs_at', data.finishs_at)
    # serializer_class = ReportSerializer1
    # parser_classes = ()
    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = self.get_serializer()
    #     kwargs["context"] = self.get_serializer_context()
    #     draft = self.request.data.copy()
    #     draft['call'] = int((self.request.data['call'])[0])
    #     draft['engineer'] = int((self.request.data['engineer'])[0])
    #     draft['status'] = ((self.request.data['status'])[0])
    #     draft['image'] = ((self.request.data['image'])[0])
    #     kwargs['data'] = draft
    #     return serializer_class(*args, *kwargs)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     call = int(request.data['call'])
    #     engineer = int(request.data['engineer'])
    #     data['call'] = call
    #     data['engineer'] = engineer
    #     return Response(data)
    #     #return super().create(request, *args, **kwargs)