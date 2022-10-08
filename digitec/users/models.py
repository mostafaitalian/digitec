from django.contrib.auth.models import AbstractUser
# from djang import settings
from django.conf import settings

from django.db.models import CharField
from django.urls import reverse
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.db import models

class NotificationToken(models.Model):
    token = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ntoken', null=True, blank=True)

    def __str__(self):
        if self.token:
            return self.user.name + ' ' +self.token
        else:
            return self.user.name

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


