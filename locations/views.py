from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from .models import Location
from inventory.models import InventoryPart, InventoryMaterial, InventoryFood
from .forms import LocationForm  # Reuse the form we discussed

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

class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    # success_url = reverse_lazy('location_tree')
    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.id})

class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'locations/location_confirm_delete.html'
    def get_success_url(self):
        if 'parent_id' in self.kwargs:
            return reverse('location_detail', kwargs={'pk': self.kwargs.get('parent_id')})
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

