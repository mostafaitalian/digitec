from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Customer, Department
from .forms import CustomerForm, DepartmentForm
from django.urls import reverse_lazy
from django.urls.base import  reverse
from .mixin import CustemerGetObjectMixin, CustemerGetObject1Mixin, CustomerActionMixin
from .utils import can_customer, check_can_add_customer
from django.contrib.auth.mixins import LoginRequiredMixin
from .bulk_machines import create_bulk
from rest_framework.generics import ListCreateAPIView
from .serializers import CustomerSerializer
from .bulk_customers import create_bulk_customers
import json
class CustomerListCreateApi(ListCreateAPIView):
    serializer_class= CustomerSerializer
    queryset = Customer.objects.all()



# Create your views here.

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name='customer_list.html'
    context_object_name='customers'
    paginate_by= 8
    query=''
    def get_queryset(self,queryset=None):
        # queryset=super().get_queryset()
        q=self.request.GET.get('q',self.query)
        
        page=self.request.GET.get('page')
        if queryset is None:
            if q and q!='all':
                queryset = Customer.objects.filter(name__icontains=q)
                print(queryset)
                return queryset
            elif q=='':
                queryset = Customer.objects.all()
                return queryset
            elif q=='all':
                queryset = Customer.objects.all()
                return queryset

        return queryset
'''    def get(self, request):
        customers = Customer.objects.all()
        return render(request, self.template_name, {'customers':customers})'''
class CustomerCreateView1(LoginRequiredMixin,CreateView):
    #fields=('name', 'slug')
    form_class = CustomerForm
    template_name = 'customer/customer_create2.html'
    success_url=reverse_lazy('customer:customer-detail')
    model = Customer
    # fields=('departments')
class CustomerCreateView(LoginRequiredMixin,CustomerActionMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_create.html'
    success_msg='you successfuly created customer'
    def get_success_url(self):
        return reverse_lazy('customer:customer-detail', kwargs={'id':self.object.id})
    
    def dispatch(self, request, *args, **kwargs):
        request = can_customer(request)
        return CreateView.dispatch(self,request, *args, **kwargs)
'''    def get_success_url(self):
        return reverse("customer:list")'''
class CustomerDetail(LoginRequiredMixin,CustemerGetObject1Mixin, DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
class CustomerUpdateView(LoginRequiredMixin,CustemerGetObject1Mixin,CustomerActionMixin, UpdateView):
    models = Customer
    #form_class = CustomerForm
    template_name  ='customer/customer_update.html'
    fields = ('name', 'slug', 'location', 'address')
    success_msg ='your customer is successfuly updated'

    def get_success_url(self):
        return reverse_lazy('customer:customer-detail', kwargs={'id':self.object.id})
        '''self.kwargs['slug'] = self.get_object().slug
        #print('hi',object.slug, self.get_object().slug)
        return reverse("customer:detail", kwargs={'slug':self.kwargs['slug']})'''
'''    def post(self, request, *args, **kwargs):
        form=CustomerForm(request.POST, instance=self.get_object())
        if form.is_valid():
            obj=form.save()
            return redirect(obj)
        else:
            form = CustomerForm(request.POST)
            return render(request,self.template_name,{'form':form})
        #return reverse_lazy('customer:detail', kwargs={'slug':self.kwargs.get('slug')} )'''
   
class CustomerDeleteView(LoginRequiredMixin,CustemerGetObject1Mixin,CustomerActionMixin, DeleteView):
    model = Customer
    template_name = 'customer/customer_delete.html'
    success_msg='your customer was deleted'
    def get_success_url(self):
        #object = self.get_object().delete()
        return reverse('customer:list')
        
'''    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        if self.machines_dep:
            self.no_of_machine = self.macines_dep.count()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)'''
class DepartmentCreateView(CreateView):
    template_name = 'customer/department_create.html'
    form_class = DepartmentForm
    model = Department


    def get_success_url(self):
        if self.object.customer:

            return reverse_lazy('customer:customer-detail', kwargs={'id':self.object.customer.id})
        else:
            return reverse_lazy('customer:customer-list')

def bulk_customers_view(request):
    customers = Customer.objects.all()
    data_list = create_bulk_customers(customers)
    da = json.loads(json.dumps(data_list,indent=4, ensure_ascii=False).encode('utf-8'))
    print(da)
    daa = [item['fields'] for item in da]
    print([d['customer_id'] for d in daa])
    print(json.loads(json.dumps(daa)))

    Customer.objects.bulk_create([Customer(**i) for i in daa])
    for c in Customer.objects.all():
        print('11111')
        if c.departments.count() == 0:
            print('22222')
            department = Department(department_name='others', customer=c)
            department.save()
    return redirect('customer:customer-list')



