from django.db import models
from django.conf import settings
from django.utils import timezone
#from machine.models import Machine
# Create your models here.
class Area(models.Model):
    name= models.CharField('area code',max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    margin = models.URLField()
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.name+self.start+self.end
        #self.save()
        super().save(*args,**kwargs)
class Engineer(models.Model):
    name=models.CharField('xerox username',max_length=255, help_text="start with 'EGD20' and followed by your number")
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='engineer', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    joining_date = models.DateField()
    no_of_calls = models.PositiveIntegerField(default=0)
    no_of_calls_pending = models.PositiveIntegerField(default=0)
    no_ofcalls_success = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
        
class EngineerReview(models.Model):
    auther = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)
    state_choices = (('pending','pending'),('published','published'),('rejected','rejected'))
    state=models.CharField(max_length=50, choices=state_choices)
    
    class Meta:
        permissions=(('can_approve_or_reject_review','can approve or reject review'),)
        
    def __str__(self):
        return self.auther.name + ' - ' + self.review
class Comment(models.Model):
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    engineer_review = models.ForeignKey(EngineerReview, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
        