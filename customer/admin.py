from django.contrib import admin
from .models import Customer, Department, CustomerOrganization, CustomerBranch
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomerOrganization)
admin.site.register(CustomerBranch)