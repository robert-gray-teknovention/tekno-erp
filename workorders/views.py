from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableView
from django_tables2 import RequestConfig

from documentation.models import TimesheetEntryDocumentation
from projects.models import Project
from .tables import WorkOrderTable, WorkEntryTable
from django.db.models import Q
from .models import WorkOrder, WorkEntry
from .forms import WorkOrderForm, WorkEntryForm, WorkEntryInlineForm
from employee.models import TimesheetUser
from timesheets.models import TimesheetPeriod


# WorkOrder views
class WorkOrderCreateView(CreateView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = "workorders/workorder_form.html"
    success_url = reverse_lazy("workorders:workorder-list")


class WorkOrderUpdateView(UpdateView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = "workorders/workorder_form.html"
    success_url = reverse_lazy("workorders:workorder-list")


class WorkOrderDeleteView(DeleteView):
    model = WorkOrder
    template_name = "workorders/workorder_confirm_delete.html"
    success_url = reverse_lazy("workorders:workorder-list")


class WorkOrderListView(LoginRequiredMixin, SingleTableView):
    model = WorkOrder
    table_class = WorkOrderTable
    template_name = "workorders/workorder_list.html"
    table_pagination = {"per_page": 20}

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(request__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class WorkOrderDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = WorkOrder
    template_name = "workorders/workorder_detail.html"
    context_object_name = "workorder"
    form_class = WorkEntryInlineForm

    def get_success_url(self):
        return reverse_lazy("workorders:workorder-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide the inline form
        if "form" not in context:
            context["form"] = self.get_form()

        # Build a table of entries for this work order
        entries = WorkEntry.objects.filter(work_order=self.object).order_by("-date_time_in")
        table = WorkEntryTable(entries)
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context["entry_table"] = table
        return context

    def post(self, request, *args, **kwargs):
        # Handle inline form submission to create a WorkEntry bound to this WorkOrder
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            entry = form.save(commit=False)
            entry.work_order = self.object
            entry.save()
            form.save_m2m()
            return redirect(self.get_success_url())
        return self.form_invalid(form)
# WorkEntry initial form user mixin
class WorkEntryInitialUserMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            ts_user = TimesheetUser.objects.get(user=self.request.user)
            initial = kwargs.get("initial", {})
            initial.setdefault("user", ts_user.pk)
            kwargs["initial"] = initial
        except TimesheetUser.DoesNotExist:
            pass
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.get_full_name()
        return initial
    
# WorkEntry views
class WorkEntryCreateView(WorkEntryInitialUserMixin, CreateView):
    model = WorkEntry
    form_class = WorkEntryForm
    template_name = "workorders/workentry_form.html"
    success_url = reverse_lazy("workorders:workentry-list")

    def get_initial(self):
        initial = super().get_initial()
        initial['work_order'] = self.request.GET.get("workorder")
        initial['project'] = Project.objects.filter(workorder__id=initial['work_order']).first()
        # initial['name'] = self.request.user.get_full_name()
        return initial

    def form_valid(self, form):
        # If a workorder pk was provided via GET or POST, bind the entry to it
        workorder_pk = self.request.POST.get("workorder") or self.request.GET.get("workorder")
        if workorder_pk and not form.instance.work_order_id:
            try:
                form.instance.work_order_id = int(workorder_pk)
            except (ValueError, TypeError):
                pass
        # Prefill user if blank: map request.user -> TimesheetUser
        if hasattr(form.instance, "user") and not form.instance.user_id:
            try:
                ts_user = TimesheetUser.objects.get(user=self.request.user)
                form.instance.user = ts_user
            except TimesheetUser.DoesNotExist:
                # leave unset; model validation will handle requiredness
                pass
        return super().form_valid(form)

    def get_success_url(self):
        # Prefer POSTed 'next', then GET 'next', else fallback to default
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url:
            return next_url
        return super().get_success_url()


class WorkEntryUpdateView(WorkEntryInitialUserMixin, UpdateView):
    model = WorkEntry
    form_class = WorkEntryForm
    template_name = "workorders/workentry_form.html"
    success_url = reverse_lazy("workorders:workentry-list")
    
    def get_success_url(self):
        # Allow redirecting back to a 'next' parameter (POST or GET)
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url:
            return next_url
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['doc_count'] = TimesheetEntryDocumentation.objects.filter(parent_id=self.object.id).count()
        print(context['doc_count'])
        return context

class WorkEntryDeleteView(DeleteView):
    model = WorkEntry
    template_name = "workorders/workentry_confirm_delete.html"
    success_url = reverse_lazy("workorders:workentry-list")

    def get_success_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url:
            return next_url
        return super().get_success_url()


class WorkEntryListView(LoginRequiredMixin, SingleTableView):
    model = WorkEntry
    table_class = WorkEntryTable
    template_name = "workorders/workentry_list.html"
    table_pagination = {"per_page": 20}

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(description__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context