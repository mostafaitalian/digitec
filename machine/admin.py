from django.contrib import admin
from .models import Machine, Category, Call
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
    #list_display = ('engineer',)
    pass