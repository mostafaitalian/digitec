from django.shortcuts import render, reverse
from django.views.generic import CreateView, ListView
from .models import Machine, Call, Category
from .forms import CreateMachineForm, CallForm, CategoryForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from .serializers import MachineSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView 
# Create your views here.

class CreateMachineView1(CreateView):
    model = Machine
    form_class = CreateMachineForm
    template_name = "machine/create_machine2.html"
    success_url = reverse_lazy('machine:create')
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
    
class MachineList(ListView):
    model = Machine
    template_name = "machine/machine_list.html"
    context_object_name = 'machine_list'
    paginated_by=4
class MachineCreateReadView(ListCreateAPIView):
    queryset=Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'slug'
class MachineUpdateReadView(RetrieveUpdateDestroyAPIView):
    queryset=Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'slug'
class CallCreateView(CreateView):
    template_name="machine/create_call.html"
    model = Call
    form_class = CallForm
    success_url = reverse_lazy("machine:call_create")


class CreateCategory(CreateView):
    template_name='machine/create_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("machine:create_category")