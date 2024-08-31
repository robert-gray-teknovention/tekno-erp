from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee.models import TimesheetUser
from projects.models import Project
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from . import models
from .forms import get_expense_form
import json

@login_required
def expense(request, type, id=0):
    # class_name = request.GET.get("type").capitalize()
    class_name = type.capitalize()
    my_class = getattr(models, class_name)
    user = TimesheetUser.objects.get(user_id=request.user.id)
    # org = TimesheetUser.objects.get(user_id=request.user.id).organization
    if request.method == 'POST':
        if id > 0:
            form = get_expense_form(class_name, request.POST, instance=my_class.objects.get(id=id))
        else:
            form = get_expense_form(class_name, request.POST)
        if form.is_valid():
            expense = form.save()
            messages.success(request, "We just added an expense")
            print(expense.__dict__)
            # return json.dumps(dict(expense), many=False)
            e = {
                'id': expense.id,
                'total_cost': expense.total_cost,
                'accrue_date': expense.accrue_date,
            }
            return JsonResponse({'success': True, 'expense': e})
        else:
            messages.error(request, "I can't add this expense.  There was an error")
            return JsonResponse({'success': False})
    else:
        print("project id ", request.GET.get('project_id'))
        form = get_expense_form(class_name, initial={'project': request.GET.get('project_id'), 'entry':
                                                     request.GET.get('entry_id')})
        e_id = id
        if e_id:
            form = get_expense_form(class_name, instance=my_class.objects.get(id=e_id))
        else:
            e_id = 0
        return render(request, 'accounting/_expense.html', {'expense_form': form, 'expense_type': class_name,
                                                            'expense_id': e_id, 'user': user,
                                                            'expense_types': dict(models.Expense.ExpenseType.choices)})


class ExpenseListView(ListView):
    template_name = 'accounting/expenses.html'
    model = models.Expense

    def get_queryset(self):
        print(self.kwargs)
        if 'partial' in self.kwargs:
            self.template_name = 'accounting/_expenses.html'
        if 'group' in self.kwargs:
            if self.kwargs['group'] == 'project':
                return models.Expense.objects.filter(project_id=self.kwargs['id'])
            if self.kwargs['group'] == 'entry':
                print("We are returning entry expenses")
                return models.Expense.objects.filter(entry_id=self.kwargs['id'])
        return models.Expense.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_types'] = dict(models.Expense.ExpenseType.choices)
        print(str(context))
        return context
