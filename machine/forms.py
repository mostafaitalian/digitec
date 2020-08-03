from django.forms import Form, ModelForm
from .models import Machine, Call, Category

class CreateMachineForm(ModelForm):
    
    
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