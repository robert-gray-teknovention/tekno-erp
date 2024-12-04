from django.contrib.auth.models import User
from timesheets.models import TimesheetUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from .forms import (
    get_company_form,
    get_item_form,
    PurchaseOrderForm,
    PurchaseItemForm,
    PurchaseOrderItemForm,
    ItemTypeForm,
    )
from .tables import ManufacturerTable, PurchaseOrderTable, PurchaseOrderItemTable
from .models import Vendor, Manufacturer, PurchaseOrder, PurchaseOrderItem, Item, Part, Service, Material, Subscription
from .models import PurchaseItem
from inventory.models import Part as InvPart
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView
from django_filters import FilterSet, CharFilter
from employee.models import TimesheetUser
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from . import tables
from . import models
from . import serializers
from . import views
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.forms import HiddenInput
from . import forms as forms
import re


class ModelFormFieldsHelperMixin():
    def hide_fields(self, form, fields):
        for f in fields:
            form.fields[f].widget = HiddenInput()
        return form


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


class MultiFieldFilterSet(FilterSet):
    search = CharFilter(method='filter_search')

    class Meta:
        fields = ['name']

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class ItemFilter(MultiFieldFilterSet):

    class Meta:
        model = Item
        fields = MultiFieldFilterSet.Meta.fields


class PartFilter(MultiFieldFilterSet):

    class Meta:
        model = Part
        fields = MultiFieldFilterSet.Meta.fields


class MaterialFilter(MultiFieldFilterSet):

    class Meta:
        model = Material
        fields = MultiFieldFilterSet.Meta.fields


class ServiceFilter(MultiFieldFilterSet):

    class Meta:
        model = Service
        fields = MultiFieldFilterSet.Meta.fields


class SubscriptionFilter(FilterSet):

    class Meta:
        model = Subscription
        fields = MultiFieldFilterSet.Meta.fields


class FilteredCompanyListView(LoginRequiredMixin, SingleTableMixin, FilterView):

    # table_class = ManufacturerTable
    # model = Manufacturer
    # filterset_class = ManufacturerFilter
    template_name = 'purchasing/companylist.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        url = self.request.build_absolute_uri()
        self.class_name = re.search(r'\/(\w+)(?:\?.*)?$', url)[1][:-1].capitalize()
        self.table_class = getattr(tables, self.class_name + 'Table')
        self.model = getattr(models, self.class_name)
        self.filterset_class = getattr(views, self.class_name + 'Filter')

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


class FilteredListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        url = self.request.build_absolute_uri()
        self.class_name = re.search(r'\/(\w+)(?:\?.*)?$', url)[1][:-1].capitalize()
        self.table_class = getattr(tables, self.class_name + 'Table')
        self.model = getattr(models, self.class_name)
        self.filterset_class = getattr(views, self.class_name + 'Filter')
        self.template_name = 'purchasing/' + self.kwargs.get('template') + 'list.html'

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model_name'] = self.class_name
        context['item_type'] = self.class_name.lower()
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

    '''def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            print("our form is valid")
            return self.form_valid(form)
        else:
            print("our form is invalid mofo")
            return self.form_invalid(form)'''

    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(id=request.user.id)
        self.org = TimesheetUser.objects.get(user=self.user).organization
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['orderer'] = self.user
        initial['organization'] = self.org
        return initial

    def get_success_url(self):
        print("We have saved")
        return reverse('po-update', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        print("Form Errors ", form.errors)

    def form_valid(self, form):
        print("The form is valid!!")
        return super().form_valid(form)


class PurchaseOrderUpdateView(LoginRequiredMixin, SingleTableMixin, ModelFormFieldsHelperMixin, UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchasing/purchaseorderupdate.html'
    table_class = PurchaseOrderItemTable
    po_id = None

    def get(self, *args, **kwargs):
        self.po_id = kwargs['pk']
        return super().get(self.request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        self.object.calculate_total()
        return initial

    def get_table_data(self):
        return self.table_class.Meta.model.objects.filter(purchase_order=self.po_id)

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pi_form = PurchaseItemForm(initial={'vendor': self.get_object().vendor})
        poi_form = PurchaseOrderItemForm(initial={'purchase_order': self.get_object()})
        context['pi_form'] = self.hide_fields(pi_form, ['vendor', 'manufacturer'])
        context['poi_form'] = self.hide_fields(poi_form, ['purchase_order', 'purchase_item'])
        return context


class PurchaseOrderItemUpdateView(LoginRequiredMixin, ModelFormFieldsHelperMixin, UpdateView):
    model = PurchaseOrderItem
    template_name = 'purchasing/purchaseorderitem_form.html'
    form_class = PurchaseOrderItemForm

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST and request.POST['delete']:
            poi = self.get_object()
            pk = poi.purchase_order.id
            poi.delete()
            return redirect(reverse('po-update', kwargs={'pk': pk}))
        return super().post(request, args, kwargs)

    def get_form(self, form_class=None):
        poi_form = self.hide_fields(super().get_form(form_class), ['purchase_order', 'purchase_item'])
        return poi_form

    def get_context_data(self, **kwargs):
        poi = self.get_object()
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['pi_form'] = self.hide_fields(PurchaseItemForm(instance=poi.purchase_item), ['vendor', 'manufacturer'])
            context['poi_form'] = self.get_form()
            context['update'] = True
        return context

    def get_success_url(self):
        return reverse('po-update', kwargs={'pk': self.object.purchase_order.id})


class PurchaseOrderItemCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseOrderItem
    form_class = PurchaseOrderItemForm
    # template_name = 'purchasing/purchaseorderupdate.html'
    table_class = PurchaseOrderItemTable
    # success_url = 'purchasing/purchaseorderupdate.html'

    def post(self, request, *args, **kwargs):
        pi_form = PurchaseItemForm(request.POST)
        purchase_item = None
        if pi_form.is_valid():
            purchase_item = pi_form.save()
        else:
            pi = self.get_purchase_item(pi_form.data['item'], pi_form.data['units'])
            pi.vendor.add(pi_form.data['vendor'])
            pi.type = pi_form.data['type']
            pi.save()
            purchase_item = pi
        form_data = request.POST.copy()
        form_data['purchase_item'] = purchase_item
        poi_form = PurchaseOrderItemForm(form_data)

        if poi_form.is_valid():
            poi_form.save()
            messages.success(request, "You purchase item has been added to the purchase order")
        else:
            messages.error(request,
                           "Your Purchase Item didn't get saved. Please make sure order item is not already listed.")
            print("POI Form Errors", poi_form.errors)
        return redirect(reverse('po-update', kwargs={'pk': poi_form.data['purchase_order']}))

    def get_success_url(self):
        return reverse('po-update', kwargs={'pk': self.object.purchase_order.id})

    def get_purchase_item(self, item, units):
        print("Item ", item)
        pi, create = PurchaseItem.objects.get_or_create(item_id=item, units=units)
        return pi


class OrganizationMixin():
    def get_organization(self, request):
        user = User.objects.get(id=request.user.id)
        return TimesheetUser.objects.get(user=user).organization


class ItemCreateView(LoginRequiredMixin, OrganizationMixin, CreateView):
    template_name = 'purchasing/_itemform.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['organization'] = super().get_organization(self.request)
        return initial

    def get_form_class(self):
        item_type = self.kwargs.get('item_type', 'Part')
        if item_type.capitalize() == 'Part':
            item_model = InvPart
        else:
            item_model = getattr(models, item_type)
        return get_item_form(item_model)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        item_type = self.kwargs.get('item_type', 'Part').capitalize()
        item_type_form = ItemTypeForm(initial={'item_type': item_type})
        context['item_type'] = item_type
        context['item_type_form'] = item_type_form
        context['form_url'] = 'item-create-form' + self.request.GET.get('url', '')
        context['update'] = False
        return context

    def get_success_url(self):
        item_type = self.kwargs.get('item_type', 'Part')
        return reverse('item-form', kwargs={'item_type': item_type})


class ItemCreateViewList(ItemCreateView):
    def get_success_url(self):
        return reverse(self.kwargs.get('item_type', 'part').lower() + 's', kwargs={'template': 'item'})


class ItemUpdateView(LoginRequiredMixin, OrganizationMixin, UpdateView):
    template_name = 'purchasing/_itemform.html'

    def dispatch(self, request, *args, **kwargs):
        # Dynamically set model based on 'item_type' in kwargs
        item_type = self.kwargs.get('item_type', 'Part')
        if item_type.capitalize() == 'Part':
            self.model = InvPart
        else:
            self.model = getattr(models, item_type)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['organization'] = self.get_organization(self.request)
        return initial

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST and request.POST['delete']:
            item = self.get_object()
            try:
                item.delete()
                messages.success(request, "Your item has been deleted")
                return redirect(reverse(kwargs['item_type'].lower()+'s', kwargs={'template': 'item'}))

            except Exception as e:
                print("exception ", e)
                messages.error(request, "Sorry your item was not deleted.")
            return redirect(reverse(kwargs['item_type'].lower()+'s', kwargs={'template': 'item'}))
        return super().post(request, args, kwargs)

    def get_form_class(self):
        # Use dynamically set model to generate form class
        return get_item_form(self.model)

    def form_invalid(self, form):
        print("you got error ", form.errors)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type = self.kwargs.get('item_type', 'Part')
        context['item_type'] = item_type
        context['item_type_form'] = ItemTypeForm(initial={'item_type': item_type})
        context['form_url'] = 'item-update-form' + self.request.GET.get('url', '')
        context['update'] = True  # Flag to indicate update mode
        return context

    def get_object(self, queryset=None):
        # Retrieve the specific object based on the model and primary key from URL kwargs
        item_id = self.kwargs.get('pk')
        return self.model.objects.get(pk=item_id)

    def get_success_url(self):
        item_type = self.kwargs.get('item_type', 'Part')
        print("We are returning from Form")
        return reverse('item-update-form', kwargs={'item_type': item_type, 'pk': self.object.pk})


class ItemUpdateViewList(ItemUpdateView):
    def get_success_url(self):
        print("We are returning from ViewList")
        return reverse(self.kwargs.get('item_type', 'part').lower() + 's', kwargs={'template': 'item'})


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
        return HttpResponseRedirect('company/' + class_name.lower()+'s')
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


@login_required
def get_items(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        results = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data = [{'id': obj.pk, 'text': str(obj)} for obj in results]
        return JsonResponse({'results': data})
