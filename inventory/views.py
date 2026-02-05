from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from . import tables
from locations.models import Location
from purchasing import views
from purchasing import models as pmodels
from .models import InventoryPart, InventoryMaterial, InventoryFood, InventoryItem, InventoryItemTransaction
from . import models
from locations.models import Location
from .forms import InventoryPartForm, InventoryMaterialForm, InventoryFoodForm
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.models import TimesheetUser
from django.core.exceptions import ImproperlyConfigured
import re
class InventoryItemModelMixin():
    def log_transaction(self):
        class_type = self.__class__.__name__.replace('View','').replace('InventoryItem','').capitalize()
        object = self.object
        print("object id for logging transaction: ", object.id)
        # Compose notes and transaction type based on action type
        if self.__class__== InventoryItemCreateView:
            transaction_type = InventoryItemTransaction.TransactionType.CREATE
            # notes = f"{class_type} quantity of {object.quantity} {object.units} of {object.item.name} in {object.location}."
        elif self.__class__== InventoryItemUpdateView:
            transaction_type = InventoryItemTransaction.TransactionType.UPDATE
            # notes = f"{class_type} quantity of {object.quantity} {object.units} of {object.item.name} in {object.location}."    
        elif self.__class__== InventoryItemDeleteView:
            transaction_type = InventoryItemTransaction.TransactionType.DELETE
            # notes =f"{class_type} {object.item.name} in {object.location}."
        InventoryItemTransaction.objects.create(
            inventory_item_id=object.id,
            location=object.location,
            item=object.item,
            quantity=object.quantity,
            units = object.units,
            transaction_type=transaction_type,
            performed_by=TimesheetUser.objects.filter(user_id=self.request.user.id).first(),
            # notes = notes
        )

        # print("Logging transaction for ", object, " of type ", class_type)
        
    def get_object(self, queryset=None):
        model_name = self.kwargs.get('model_name').lower()
        if model_name == 'part':
            self.model = models.InventoryPart
        if model_name == 'material':
            self.model = models.InventoryMaterial
        if model_name == 'food':
            self.model =models.InventoryFood
        return super().get_object(queryset)

    def get_form_class(self):
        model_name = self.kwargs.get('model_name').lower()
        if model_name == 'part':
            # self.model = models.InventoryPart
            return InventoryPartForm
        elif model_name == 'material':
            # self.model = models.InventoryMaterial
            return InventoryMaterialForm
        elif model_name == 'food':
            return InventoryFoodForm
    
        else:
            raise Http404('Model not found')

    def get_success_url(self):
        if 'success_url' in self.kwargs:
            if 'initial_id' in self.kwargs:
                return reverse(self.kwargs.get('success_url'), kwargs={'pk': self.kwargs.get('initial_id')})
            else:
                return reverse(self.kwargs.get('success_url'))
        return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.kwargs.get("model_name")
        if 'initial_id' in self.kwargs:
            context['initial_id'] = self.kwargs.get("initial_id")
        if 'success_url' in self.kwargs:
            context['success_url'] = self.kwargs.get("success_url")
        if self.__class__== InventoryItemCreateView:
            context['form_type'] = 'create'
        elif self.__class__== InventoryItemTransferView:
            context['form_type'] = 'transfer'
            context['pk'] = self.kwargs.get('pk')
        else:
            context['form_type'] = 'update'
            context['pk'] = self.kwargs.get('pk')
        context['item_search_select'] = {'id': 'item'}
        context['location_search_select'] = {'id': 'location'}
        return context
    
    def form_valid(self, form):
        # the form_valid method in this mixin logs the transaction after saving the form for create, update, and delete views. Transfers are handled separately.
        if self.__class__ == InventoryItemCreateView:
            response = super().form_valid(form)
            self.log_transaction()
            return response
        else:
            # response = super().form_valid(form)
            self.log_transaction()
            return super().form_valid(form)

class InventoryItemCreateView(InventoryItemModelMixin, CreateView):
    # fields = ['field1', 'field2'] # Fields to include in the form
    # form_class = InventoryPartForm
    template_name = 'inventory/_item_form.html'
    success_url = 'inventory_list'
    
    def get_initial(self): #work on assigning initial data for part or location.
        initial = super().get_initial()
        if 'initial_type' in self.kwargs:
            if self.kwargs.get('initial_type').lower() == 'location':
                initial['location'] = self.kwargs.get('initial_id')
            
            elif self.kwargs.get('initial_type').lower() in ['food', 'part', 'material']:
                initial['item'] = self.kwargs.get('initial_id')
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.disable_field = self.kwargs.pop('initial_type', None)
        print("disable field ", self.disable_field)
        if self.disable_field:
            if self.disable_field.lower() in ['part', 'material', 'food']:
                self.disable_field = 'item'
            kwargs['disabled_fields'] = [self.disable_field]
        return kwargs
    
    def form_invalid(self, form):
        print("❌ Form is invalid!")
        print("Errors:", form.errors)
        print("POST data:", self.request.POST)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class InventoryItemUpdateView(InventoryItemModelMixin, UpdateView):
    model = models.InventoryMaterial
    # fields = ['field1', 'field2']
    template_name = 'inventory/_item_form.html'
    # success_url = 'inventory/list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['disabled_fields'] = ['item', 'location']
        return kwargs
    
class InventoryItemTransferView(InventoryItemModelMixin, UpdateView):
    model = models.InventoryPart
    template_name = 'inventory/_item_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['disabled_fields'] = ['item']
        return kwargs
    
    def form_valid(self, form):
        # Transfer logic is handled in the form_valid method of this view.

        return super().form_valid(form)

class InventoryItemDeleteView(InventoryItemModelMixin, DeleteView):
    model = models.InventoryPart
    template_name = 'inventory/inventoryitem_confirm_delete.html'
    def get_form_class(self):
        # Returning basde DeleteView form class because we don't want a custom form for delete view.
        return DeleteView.get_form_class(self)

class InventoryFilteredListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        url = self.request.build_absolute_uri()
        #self.class_name = re.search(r'\/(\w+)(?:\?.*)?$', url)[1][:-1].capitalize()
        if 'model_name' in self.kwargs:
            self.class_name = self.kwargs['model_name'].capitalize()
        else:
            self.class_name = 'Part'
        self.table_class = getattr(tables, self.class_name + 'Table')
        self.model = getattr(models, self.class_name)
        self.filterset_class = getattr(views, self.class_name + 'Filter')
        self.template_name = 'inventory/inventory_list.html'

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

class InventoryItemListView(SingleTableMixin, ListView):
    table_class = tables.InventoryItemTable
    template_name = 'inventory/inventory_item_list.html'
    def get_queryset(self):
        self.model = getattr(models, "Inventory" + self.kwargs.get('model_name').capitalize())
            
        if 'lookup_type' and 'lookup_id' in self.kwargs:
            if self.kwargs['lookup_type'].lower() == 'location':
                return self.model.objects.filter(location_id=self.kwargs.get("lookup_id"))
            if self.kwargs['lookup_type'].lower() == 'item':
                return self.model.objects.filter(item_id=self.kwargs.get("lookup_id"))
        return self.model.objects.all()
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.kwargs.get('model_name')
        if 'lookup_type' and 'lookup_id' in self.kwargs:
            if self.kwargs['lookup_type'].lower() == 'location':
                context['object'] = Location.objects.get(id=self.kwargs['lookup_id'])
            if self.kwargs['lookup_type'].lower() == 'item':
                context['object'] = getattr(pmodels, self.kwargs['lookup_type'].capitalize()).objects.get(id= self.kwargs['lookup_id'])
        return context

class InventoryItemListByItemIdView(InventoryItemListView):
    def get_queryset(self):
        inventory_items = None
        if 'pk' in self.kwargs:
            self.item = pmodels.Item.objects.get(id=self.kwargs['pk'])
            inventory_items = getattr(models, 'Inventory' + self.item.polymorphic_ctype.name.capitalize()).objects.filter(item = self.item)
        return inventory_items.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.item.polymorphic_ctype.name
        context['lookup_id'] = self.item.id
        context['lookup_type'] = 'item'
        context['object'] = self.item
        return context

def get_items(request):
    from purchasing import models
    if request.method == 'GET':
        item_type =request.GET.get('item_type','part')
        query = request.GET.get('query', '')
        results = getattr(models, item_type.capitalize()).objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data = [{'id': obj.pk, 'text': str(obj)} for obj in results]
        return JsonResponse({'results': data})


class TempInventoryItemTransferView(LoginRequiredMixin, InventoryItemModelMixin,UpdateView):
    """
    View to transfer inventory items between locations.
    Adds/updates item in new location and subtracts from old location.
    """
    model = models.InventoryItem
    template_name = 'inventory/transfer_item_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs.get('model_name', 'part').lower()
        context['available_locations'] = Location.objects.exclude(id=self.object.location.id)
        context['source_location'] = self.object.location
        context['item'] = self.object.item
        return context
    
    def form_valid(self, form):
        """
        Handle the transfer logic:
        1. Get the quantity to transfer
        2. Get the destination location from POST
        3. Subtract from source location
        4. Add/update in destination location
        5. Log transactions
        """
        from django.db import transaction
        from django.contrib.auth.models import User
        
        source_inventory = self.object
        transfer_quantity = form.cleaned_data['quantity']
        destination_location_id = self.request.POST.get('destination_location')
        
        if not destination_location_id:
            form.add_error(None, "Please select a destination location.")
            return self.form_invalid(form)
        
        # Validate transfer quantity
        if transfer_quantity <= 0:
            form.add_error('quantity', "Transfer quantity must be greater than 0.")
            return self.form_invalid(form)
        
        if transfer_quantity > source_inventory.quantity:
            form.add_error('quantity', f"Cannot transfer more than available quantity ({source_inventory.quantity}).")
            return self.form_invalid(form)
        
        try:
            with transaction.atomic():
                destination_location = Location.objects.get(id=destination_location_id)
                model_name = self.kwargs.get('model_name', 'part').lower()
                model_class = self.model
                
                # Update source location - subtract quantity
                source_inventory.quantity -= transfer_quantity
                source_inventory.save()
                
                # Add or update destination location
                destination_inventory, created = model_class.objects.get_or_create(
                    item=source_inventory.item,
                    location=destination_location,
                    defaults={
                        'quantity': transfer_quantity,
                        'units': source_inventory.units
                    }
                )
                
                if not created:
                    destination_inventory.quantity += transfer_quantity
                    destination_inventory.save()
                
                # Log source transfer transaction
                current_user = TimesheetUser.objects.filter(user_id=self.request.user.id).first()
                
                InventoryItemTransaction.objects.create(
                    location=source_inventory.location,
                    item=source_inventory.item,
                    quantity=transfer_quantity,
                    transaction_type=InventoryItemTransaction.TransactionType.SOURCE_TRANSFER,
                    performed_by=current_user,
                    notes=f"Transferred {transfer_quantity} {source_inventory.units} to {destination_location.name}"
                )
                
                # Log destination transfer transaction
                InventoryItemTransaction.objects.create(
                    location=destination_location,
                    item=source_inventory.item,
                    quantity=transfer_quantity,
                    transaction_type=InventoryItemTransaction.TransactionType.DESTINATION_TRANSFER,
                    performed_by=current_user,
                    notes=f"Received {transfer_quantity} {source_inventory.units} from {source_inventory.location.name}"
                )
        
        except Location.DoesNotExist:
            form.add_error(None, "Selected destination location does not exist.")
            return self.form_invalid(form)
        except Exception as e:
            form.add_error(None, f"Transfer failed: {str(e)}")
            return self.form_invalid(form)
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('inventory_item_list', kwargs={
            'lookup_type': 'location',
            'lookup_id': self.object.location.id,
            'model_name': self.kwargs.get('model_name', 'part').lower()
        })