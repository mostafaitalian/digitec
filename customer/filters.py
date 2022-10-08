from .models import Customer
from django import forms
from engineer.models import Engineer
import django_filters

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    engineers = django_filters.ModelMultipleChoiceFilter(queryset=Engineer.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Customer
        fields= ['name', 'customer_id', 'engineers']
