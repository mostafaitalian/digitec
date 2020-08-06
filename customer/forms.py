from django.forms import ModelForm
from .models import Customer, Department

class CustomerForm(ModelForm):
    
    
    class Meta:
        model = Customer
        fields = '__all__'


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'        