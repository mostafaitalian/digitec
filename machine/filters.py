from .models import Machine, Call, Report
import django_filters

class MachineFilter(django_filters.FilterSet):
    class Meta:
        model=Machine
        fields=['serial', 'machine_category', 'machine_model', 'area', 'customer', 'department', 'contract']

class CallFilter(django_filters.FilterSet):
    # year_created = django_filters.NumberFilter(name='created_date', lookup_expr='year')
    # month_created = django_filters.NumberFilter(name='created_date', lookup_expr='month')
    # year_created = django_filters.NumberFilter(name='created_date', lookup_expr='year')


    class Meta:
        model=Call
        fields = ['notification_number', 'engineer', 'customer', 'machine', 'is_assigned', 'status', 'created_date', 'updated_date']

class ReportFilter(django_filters.FilterSet):
    # year_created = django_filters.NumberFilter(name='created_date', lookup_expr='year')
    # month_created = django_filters.NumberFilter(name='created_date', lookup_expr='month')
    # year_created = django_filters.NumberFilter(name='created_date', lookup_expr='year')


    class Meta:
        model=Report
        fields = ['call', 'engineer', 'billing_meter_black', 'billing_meter_color', 'billing_meter_total', 'billing_meter1', 'billing_meter2', 'summary', 'notes_for_dispatcher', 'created_date', 'updated_date']