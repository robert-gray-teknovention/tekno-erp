from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableView
from .tables import WorkOrderTable, WorkEntryTable
from django.db.models import Q
from .models import WorkOrder, WorkEntry
from .forms import WorkOrderForm, WorkEntryForm


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


# WorkEntry views
class WorkEntryCreateView(CreateView):
    model = WorkEntry
    form_class = WorkEntryForm
    template_name = "workorders/workentry_form.html"
    success_url = reverse_lazy("workorders:workentry-list")


class WorkEntryUpdateView(UpdateView):
    model = WorkEntry
    form_class = WorkEntryForm
    template_name = "workorders/workentry_form.html"
    success_url = reverse_lazy("workorders:workentry-list")


class WorkEntryDeleteView(DeleteView):
    model = WorkEntry
    template_name = "workorders/workentry_confirm_delete.html"
    success_url = reverse_lazy("workorders:workentry-list")


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