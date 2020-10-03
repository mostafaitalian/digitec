from django.contrib import admin
from .models import Machine, Category, Call, Report, Contract, EngineerReview, Comment, ImageReview
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

admin.site.register(Report)
admin.site.register(Contract)
admin.site.register(EngineerReview)
admin.site.register(Comment)
admin.site.register(ImageReview)
