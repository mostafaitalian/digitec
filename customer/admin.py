from django.contrib import admin
from .models import Customer, Department
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass