from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(auto_now=True)
    finished_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contributors = models.ManyToManyField(User, related_name='projects')
    organizations = models.ManyToManyField(Organization, related_name='projects')
