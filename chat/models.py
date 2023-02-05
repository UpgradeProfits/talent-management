from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class chatMessages(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
