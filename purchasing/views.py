from django.contrib.auth.models import User
from timesheets.models import TimesheetUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from .forms import get_company_form, get_item_form, PurchaseOrderForm, PurchaseItemForm, PurchaseOrderItemForm
from .tables import ManufacturerTable, PurchaseOrderTable, PurchaseOrderItemTable
from .models import Vendor, Manufacturer, PurchaseOrder, PurchaseOrderItem
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView
from django_filters import FilterSet
from employee.models import TimesheetUser
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from . import tables
from . import models
from . import serializers
from . import views
from django.urls import reverse
from django.contrib import messages
import re


class VendorFilter(FilterSet):

    class Meta:
        model = Vendor
        # organizations = ChoiceFilter(choices=FILTER_CHOICES)
        fields = {"name": ["icontains"]}
        # fields = {"name": ["icontains"], "organizations": ["exact"]}


class ManufacturerFilter(FilterSet):

    class Meta:
        model = Manufacturer
        fields = {'name': ["icontains"]}


class FilteredCompanyListView(LoginRequiredMixin, SingleTableMixin, FilterView):

    table_class = ManufacturerTable
    # model = Manufacturer
    # filterset_class = ManufacturerFilter
    template_name = 'purchasing/vendorlist.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        url = self.request.build_absolute_uri()
        self.class_name = re.search(r'\/(\w+)(?:\?.*)?$', url)[1][:-1].capitalize()
        self.table_class = getattr(tables, self.class_name + 'Table')
        self.model = getattr(models, self.class_name)
        self.filterset_class = getattr(views, self.class_name + 'Filter')
        self.template_name = 'purchasing/companylist.html'

    def get_table_data(self):
        """
        Overriden method that adds an extra filter for organization
        """
        # class_name = self.request.build_absolute_uri().split('/')[-1].title()[:-1]
        org_id = TimesheetUser.objects.get(user_id=self.request.user.id).organization.id
        if self.table_data is not None:
            return self.table_data

        elif hasattr(self, "object_list"):
            return self.object_list.filter(organization__id=org_id)
        elif hasattr(self, "get_queryset"):
            return self.get_queryset()
        view_name = type(self).__name__
        raise ImproperlyConfigured(f"Table data was not specified. Define {view_name}.table_data")

    def get_context_data(self, *args, **kwargs):
        context = super(FilteredCompanyListView, self).get_context_data(*args, **kwargs)
        context['model_name'] = self.class_name
        context['company_type'] = self.class_name.lower()
        return context


class PurchaseOrderListView(LoginRequiredMixin, SingleTableView):
    model = PurchaseOrder
    table_class = PurchaseOrderTable
    template_name = 'purchasing/purchaseorderlist.html'


class PurchaseOrderCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchasing/purchaseordercreate.html'
    user = None
    org = None

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(id=request.user.id)
        self.org = TimesheetUser.objects.get(user=self.user).organization
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['orderer'] = self.user
        initial['organization'] = self.org
        return initial

    def get_success_url(self):
        return reverse('po-update', kwargs={'pk': self.object.pk})


class PurchaseOrderUpdateView(LoginRequiredMixin, SingleTableMixin, UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchasing/purchaseorderupdate.html'
    table_class = PurchaseOrderItemTable
    po_id = None

    def get(self, *args, **kwargs):
        self.po_id = kwargs['pk']
        return super().get(self.request, *args, **kwargs)

    def get_table_data(self):
        return self.table_class.Meta.model.objects.filter(purchase_order=self.po_id)

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pi_form'] = PurchaseItemForm()
        context['poi_form'] = PurchaseOrderItemForm(initial={'purchase_order': self.get_object()})
        return context


class PurchaseOrderItemCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseOrderItem
    form_class = PurchaseOrderItemForm
    # template_name = 'purchasing/purchaseorderupdate.html'
    table_class = PurchaseOrderItemTable
    # success_url = 'purchasing/purchaseorderupdate.html'

    def form_invalid(self, form):
        print("We have an invalid form!!!!!", form.data['purchase_order'])
        messages.error(self.request, "We have an issue with your item.  It did not get saved")
        return redirect(reverse('po-update', kwargs={'pk': form.data['purchase_order']}))
        # return super().form_invalid(form)

    def get_success_url(self):
        print(str(self.object.purchase_order.id))
        return reverse('po-update', kwargs={'pk': self.object.purchase_order.id})


@login_required
def company(request):
    class_name = request.GET.get("type").capitalize()
    company_class = getattr(models, class_name)
    # form = getattr(forms, class_name + 'Form')
    # form = None
    org = TimesheetUser.objects.get(user_id=request.user.id).organization
    if request.method == 'POST':
        if request.GET.get("v_id"):
            c_form = get_company_form(company_class, request.POST,
                                      instance=company_class.objects.get(id=request.GET.get("v_id")))
        else:
            c_form = get_company_form(company_class, request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, "We just added " + request.POST['name'] + " to the vendor list.")
        else:
            messages.error(request, "I can't add " + request.POST['name'] + " because it already exists.")
        return HttpResponseRedirect(class_name.lower()+'s')
    else:
        c_form = get_company_form(company_class, initial={'organization': org})
        v_id = request.GET.get('v_id')
        exist = False
        if v_id:
            c_form = get_company_form(company_class, instance=company_class.objects.get(id=v_id))
            exist = True
            # vendor_form.instance = Vendor.objects.get(id=v_id)
        return render(request, 'purchasing/company.html', {'company_form': c_form, 'company_type': class_name,
                                                           'exist': exist})


@login_required
def CompanyApiView(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        class_name = request.GET.get('class')
        company = getattr(models, class_name)
        serializer = getattr(serializers, class_name + 'Serializer')(company.objects.filter(name__icontains=name),
                                                                     many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse(status=400)


@login_required
def dashboard(request):
    if request.method == 'GET':
        context = {
            'test': 'test',
        }
        return render(request, 'purchasing/dashboard.html', context)
