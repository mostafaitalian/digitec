from django.forms import Form, ModelForm
from .models import Machine, Call, Category,Report
from customer.models import Department
from django import forms
from engineer.models import Engineer
from itertools import chain
from django.db.models import Q


class CreateMachineForm(ModelForm):
    
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    # def __init__(self, instance=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     print(self.fields)
    #     if self.fields['customer']:
    #         customer = self.fields['customer']
    #     #customer_i = customer
        
    #     if(customer is None):
    #         self.fields['department'].queryset=Department.objects.all()
    #     else:
    #         self.fields['department'].querset=Department.objects.filter(customer__name=customer)
    class Meta:
        model = Machine
        fields = '__all__'
class CallForm(ModelForm):
    
    class Meta:
        model = Call
        fields = '__all__'

class CategoryForm(ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__' 

class ReportForm(ModelForm):
    call = forms.ModelChoiceField(queryset=None)
    def __init__(self):
        self.fields['call'].queryset = Call.objects.filter(status='pending')
    class Meta:
        model = Report
        fields = '__all__'

class ReportForm1(ModelForm):
    
    call = forms.ModelChoiceField(queryset=Call.objects.filter(Q(status='pending')|Q(status='unassigned')))
    customer_name = forms.CharField(max_length=50)
    engineer = forms.ModelChoiceField(queryset=Engineer.objects.all())

    class Meta:
        model=Report
        fields='__all__'