from django.contrib import admin
from .models import Machine, Category, Call, Report, Contract, EngineerReview, Comment, ImageReview, FileReview, ImageReport, FileReport, Contact
# Register your models here.
from import_export.admin import ImportExportModelAdmin
@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin):
    list_display = ('serial','machine_model','machine_category','machine_points', 'customer', 'area')
    list_filter=('area', 'machine_category', 'customer', 'machine_model')
    search_fields = ('area', 'machine_model', 'machine_category', 'customer')
    # prepopulated_fields = {'slug':('serial', 'serial2')}
    pass
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_type',)
@admin.register(Call)
class CallAdmin(ImportExportModelAdmin):
    list_display = ('notification_number','engineer','machine', 'status')
    # list_filter=('engineer', 'machine', 'customer')
    # search_fields = ('engineer', 'machine', 'customer')
    # inlines=['call_contacts']
    pass
@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    list_display=('mobile', 'call', 'first_name', 'last_name')
    list_filter = ('call','first_name')
    # list_display_links=('first_name', 'last_name')
    list_editable = ('first_name', 'last_name')

@admin.register(Report)
class ReportAdmin(ImportExportModelAdmin):
    def get_machine(self,obj):
        return obj.call.machine
    list_display = ('id', 'call', 'get_machine','engineer', 'billing_meter_black', 'billing_meter_color', 'billing_meter_total', 'image', 'report_copy', 'status', 'summary')
    list_filter=('engineer', 'call', 'status')
    search_fields = ('engineer', 'status', 'customer')
    # inlines=['call_contacts']
    pass
    
# admin.site.register(Report)
admin.site.register(Contract)
admin.site.register(EngineerReview)
admin.site.register(Comment)
admin.site.register(ImageReview)
admin.site.register(ImageReport)