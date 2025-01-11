from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(auto_now=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contributors = models.ManyToManyField(User, related_name='projects', blank=True)
    organizations = models.ManyToManyField(Organization, related_name='projects', blank=True)

    def __str__(self):
        return self.name


class ProjectDocumentation(models.Model):
    project = models.ForeignKey(Project, related_name='documentation', on_delete=models.CASCADE)
    file = models.FileField(upload_to="documentation/")
    description = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documentation for {self.project.name}"
