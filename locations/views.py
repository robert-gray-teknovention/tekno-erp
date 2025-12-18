from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
)
from .models import Location
from inventory.models import InventoryPart, InventoryMaterial, InventoryFood
from .forms import LocationForm  # Reuse the form we discussed
from django.http import JsonResponse
from django.db.models import Q
class LocationListView(ListView):
    model = Location
    context_object_name = 'locations'
    template_name = 'locations/location_tree.html'  # hierarchical list

    def get_queryset(self):
        return Location.objects.filter(parent__isnull=True)  # Only top-level

class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    success_url = reverse_lazy('location_tree')
    def get_initial(self):
        initial = super().get_initial()
        initial["parent"] = self.kwargs.get('parent_id')
        return initial

    def get_success_url(self):
        if 'parent_id' in self.kwargs:
            return reverse('location_detail', kwargs={'pk': self.kwargs.get('parent_id')})
        return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        if 'parent_id' in self.kwargs:
            context['parent_id'] = self.kwargs.get('parent_id')
        context['location_search_select'] = {'id': 'parent'}
        return context


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    # success_url = reverse_lazy('location_tree')
    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_search_select'] = {'id': 'parent'}
        return context

class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'locations/location_confirm_delete.html'
    parent_id = None
    def form_valid(self, form):
        self.parent_id = self.object.parent.id
        return super().form_valid(form)
            
    def get_success_url(self):
        if self.parent_id:
            return reverse('location_detail', kwargs={'pk': self.parent_id })
        return reverse('location_tree')

class LocationDetailView(DetailView):
    model = Location
    template_name = 'locations/location_detail.html'
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.object

        # Include all inventory items for this location
        context['inventory_items'] = {
            'parts': InventoryPart.objects.filter(location=location),
            'materials': InventoryMaterial.objects.filter(location=location),
            'foods': InventoryFood.objects.filter(location=location),
        }
        # Generate breadcrumb trail by walking up parent tree
        breadcrumbs = []
        current = location
        while current:
            breadcrumbs.insert(0, current)
            current = current.parent
        context['breadcrumbs'] = breadcrumbs
        context['children'] = location.children.all()
        # print("Child nunbers " + str(location.children.all().count()))
        return context

class LocationCopyView(UpdateView):
    model = Location
    template_name = 'locations/location_confirm_copy.html'
    form_class = LocationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['parent'] = None
        query_set = Location.objects.filter(name = 'Templates')
        if query_set.exists:
            initial['parent'] = query_set.first() 
        return initial

    def form_valid(self, form):
        from django.http import HttpResponseRedirect        
        form.instance.duplicate()
        return HttpResponseRedirect(reverse('location_tree'))
    
def get_locations(request):
    if request.method == 'GET':
        query = request.GET.get('query','')
        results = Location.objects.filter(Q(full_path__icontains=query) | Q(description__icontains=query))
        data = [{'id': obj.pk, 'text': str(obj)} for obj in results]
        return JsonResponse({'results': data})




