from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import InventoryPart, InventoryMaterial, InventoryFood
from . import models
from locations.models import Location
from .forms import InventoryPartForm, InventoryMaterialForm, InventoryFoodForm
from django.http import Http404
from django.db.models import Q
class InventoryItemModelMixin():
    
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
        print("WE have succeeded with the form.")
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
        else:
            context['form_type'] = 'update'
            print("We are updating with pk of ", self.kwargs.get('pk'))
            context['pk'] = self.kwargs.get('pk')
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
            
            elif self.kwargs.get('initial_type').lower() in ['part', 'material', 'food']:
                initial['item'] = self.kwargs.get('initial_id')
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.disable_field = self.kwargs.pop('initial_type', None)
        if self.disable_field:
            if self.disable_field in ['part', 'material', 'food']:
                self.disable_field = 'item'
            kwargs['disabled_fields'] = [self.disable_field]
        return kwargs
    
    def form_invalid(self, form):
        print("❌ Form is invalid!")
        print("Errors:", form.errors)
        print("POST data:", self.request.POST)
        return super().form_invalid(form)
    



class InventoryItemUpdateView(InventoryItemModelMixin, UpdateView):
    model = models.InventoryMaterial
    # fields = ['field1', 'field2']
    template_name = 'inventory/_item_form.html'
    success_url = 'inventory/list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['disabled_fields'] = ['item', 'location']
        return kwargs
    

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


def get_items(request):
    from purchasing import models
    if request.method == 'GET':
        item_type =request.GET.get('item_type','part')
        query = request.GET.get('query', '')
        results = getattr(models, item_type.capitalize()).objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data = [{'id': obj.pk, 'text': str(obj)} for obj in results]
        #for d in data:
        #    print ("id ", d['id'])
        return JsonResponse({'results': data})
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