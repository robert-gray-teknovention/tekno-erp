from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from .forms import get_company_form
from .tables import VendorTable, ManufacturerTable
from .models import Vendor, Manufacturer
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_filters import FilterSet
from employee.models import TimesheetUser
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from . import tables
from . import models
from . import serializers
from . import views
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
