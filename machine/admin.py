from django.contrib import admin
from .models import Machine, Category, Call, Report, Contract, EngineerReview, Comment, ImageReview, FileReview, ImageReport, FileReport, Contact
# Register your models here.

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('serial', 'serial2')}
    pass
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_type',)
@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('notification_number','engineer','machine')
    list_filter=('engineer', 'machine', 'customer')
    search_fields = ('engineer', 'machine', 'customer')
    # inlines=['call_contacts']
    pass
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('mobile', 'call', 'first_name', 'last_name')
    list_filter = ('call','first_name')
    # list_display_links=('first_name', 'last_name')
    list_editable = ('first_name', 'last_name')


    
admin.site.register(Report)
admin.site.register(Contract)
admin.site.register(EngineerReview)
admin.site.register(Comment)
admin.site.register(ImageReview)
