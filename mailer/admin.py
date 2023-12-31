from django.contrib import admin
from .models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ('sender', 'date_sent', 'subject', 'recipients')


admin.site.register(Email, EmailAdmin)
