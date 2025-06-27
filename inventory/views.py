from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import InventoryPart, InventoryMaterial
from . import models
from locations.models import Location
from .forms import InventoryPartForm, InventoryMaterialForm
from django.http import Http404
class InventoryItemModelMixin():
    
    def get_form_class(self):
        model_name = self.kwargs.get('model_name').lower()
        if model_name == 'part':
            self.model = models.InventoryPart
            return InventoryPartForm
        elif model_name == 'material':
            self.model = models.InventoryMaterial
            return InventoryMaterialForm
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
        return context
    

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
                return initial
        return initial


class InventoryItemUpdateView(InventoryItemModelMixin, UpdateView):
    model = models.InventoryPart
    # fields = ['field1', 'field2']
    template_name = 'inventory/_item_form.html'
    success_url = 'inventory/list.html'

class InventoryItemDeleteView(DeleteView):
    model = models.InventoryPart
    success_url = '/success/'

class InventoryItemListView(ListView):
    # model = InventoryPart
    template_name = 'inventory/inventory_list.html'
    def get_queryset(self):
        try:
            self.model = getattr(models, "Inventory" + self.kwargs.get('model_name').capitalize())
            
            return self.model.objects.all()
        except:
            raise Http404("Model not found.")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.kwargs.get('model_name')
        return context

'''class InventoryMaterialCreate(CreateView):
    model = InventoryMaterial
    fields = ['field1', 'field2'] # Fields to include in the form
    success_url = '/success/'     # URL to redirect after successful creation

class InventoryMaterialUpdate(UpdateView):
    model = InventoryMaterial
    fields = ['field1', 'field2']
    success_url = '/success/'

class InventoryMaterialDelete(DeleteView):
    model = InventoryMaterial
    success_url = '/success/'
    '''