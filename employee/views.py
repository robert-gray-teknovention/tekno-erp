from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee
from organizations.models import Organization


def index(request):
    orgs = Organization.objects.all().order_by('name')
    context = {
            'orgs': orgs
    }
    return render(request, 'index.html', context)


def employees(request):
    # employee = Employee.objects.all()
    # return render(request, 'employee.html', {'employee': employee})
    if request.method == 'POST':
        emp_id = request.POST['emp_id']
        emp_name = request.POST['emp_name']
        date_time_in = request.POST['date_time_in']
        date_time_out = request.POST['date_time_out']
        duration = request.POST['duration']
        hourly_rate = request.POST['hourly_rate']

        employee = Employee(emp_id=emp_id, emp_name=emp_name, date_time_in=date_time_in,
                            date_time_out=date_time_out, duration=duration, hourly_rate=hourly_rate)
        employee.save()

        messages.success(request, 'Time Sheet added successfully')

        return redirect('/accounts/dashboard')
