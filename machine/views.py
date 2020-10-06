from django.shortcuts import render, reverse
from django.views.generic import CreateView, ListView, DetailView
from .models import Machine, Call, Category, Report
from .forms import CreateMachineForm, CallForm, CategoryForm, ReportForm, ReportForm1
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from engineer.models import Engineer
from customer.models import Department, Customer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import MachineSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView 
# Create your views here.
import json



class CreateMachineView1(CreateView):
    model = Machine
    form_class = CreateMachineForm
    template_name = "machine/create_machine2.html"
    success_url = reverse_lazy('customer:customer-list')
    def get(self, request):
        # customer = customer_slug
        
        customer_s = request.GET.get('slug', None)
        if customer_s:
            customer_instance = Customer.objects.get(slug__startswith=customer_s)
            form = self.form_class(initial={'customer':Customer.objects.get(slug__startswith=customer_s), 'area':customer_instance.area, 'engineers': Engineer.objects.filter(area=customer_instance.area)})
            form.fields['department'].queryset = Department.objects.filter(customer__slug__startswith=customer_s)
            
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
    paginate_by=4
class MachineCreateReadView(ListCreateAPIView):
    # queryset=Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'slug'
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
        call = Call.objects.get(pk=self.kwargs['pk'])
        if self.request.user.is_superuser:
            print(kwargs)
            return call
        elif self.request.user == call.engineer.user:
            return call
        else:

            return call
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ReportForm1()
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
