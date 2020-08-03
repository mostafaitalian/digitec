from django.contrib import admin
from .models import Area, Engineer,EngineerReview, Comment
# Register your models here.
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass

@admin.register(Engineer)
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(EngineerReview)
admin.site.register(Comment)