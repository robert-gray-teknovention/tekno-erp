from django.db import models

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.name
