from django.forms import ModelForm
from .models import Customer, Department
from django import forms
from engineer.models import Area

class CustomerForm(ModelForm):
    slug = forms.SlugField(required=False)
    


    class Meta:
        model = Customer
        fields = '__all__'


class DepartmentForm(ModelForm):

    
    class Meta:
        model = Department
        fields = '__all__'        