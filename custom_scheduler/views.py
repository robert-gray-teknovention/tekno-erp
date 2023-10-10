# from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from custom_scheduler.forms import CustomEventForm, StaffTimeForm
from django.views.generic.edit import FormView
from django.http import JsonResponse


# Create your views here.
class CalendarView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        form = CustomEventForm()
        staffingForm = StaffTimeForm(auto_id="id_staff_%s")
        # form = StaffTimeForm()
        context = super(CalendarView, self).get_context_data(*args, **kwargs)
        context['eventForm'] = form
        context['staffingForm'] = staffingForm
        context['base_url'] = self.request.build_absolute_uri()
        print(context['base_url'])
        return context


class EventViewAddChangeDelete(FormView):
    form = CustomEventForm

    def post(self, request, *args, **kwargs):
        print("yay we are posting our data")
        return JsonResponse({"message": "Your event has been added to the calendar"})

    def delete(self, request, *args, **kwargs):
        print("We are deleting this event")
        return JsonResponse({"message": "Your event has been deleted from the calendar"})
