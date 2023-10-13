from django.db import models

# Create your models here.


class PasswordReset(models.Model):
    email = models.EmailField(max_length=100)
    onetime_code = models.CharField(max_length=10)
    used = models.BooleanField(default=False)
