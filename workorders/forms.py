from django import forms

from employee.models import AlternateWageCode
from .models import WorkEntry, WorkOrder

class WorkOrderForm(forms.ModelForm):
    """
    ModelForm for the Workorder model.
    - Uses all model fields by default.
    - Adds minimal widget improvements (textarea for long text, date inputs).
    - Adds a small initializer to apply a common CSS class to widgets.
    """

    class Meta:
        model = WorkOrder
        fields = "__all__"
        widgets = {
            # common sensible defaults; keys that don't exist on the model are ignored by Django
            "request": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "scheduled_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "assigned_to": forms.SelectMultiple(attrs={"size": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply a common CSS class to all widgets to ease styling (e.g., Bootstrap)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            classes = (existing + " form-control").strip()
            field.widget.attrs["class"] = classes

        # Example: make some fields optional/required based on model or runtime context
        # if "assigned_to" in self.fields:
        #     self.fields["assigned_to"].required = False

    # Optional: add model-agnostic cleaning hook
    def clean(self):
        cleaned = super().clean()
        # Place shared cross-field validation here. Example template:
        # start = cleaned.get("start_date")
        # end = cleaned.get("end_date")
        # if start and end and end < start:
        #     self.add_error("end_date", "End date cannot be before start date.")
        return cleaned

class WorkEntryForm(forms.ModelForm):
    """
    ModelForm for the WorkEntry model.
    - Uses all model fields by default.
    - Adds minimal widget improvements (textarea for long text, date/time inputs).
    - Applies a common CSS class to widgets.
    """
    # Add user name field
    name = forms.CharField(
        max_length=150,
        required=False,
    )
    # Add field for alternate wage code if needed in the future
    alternate_wage_code = forms.ModelChoiceField(
         queryset=AlternateWageCode.objects.all(),
         required=False,
         help_text="Select an alternate wage code for this entry, if applicable.",
    )
    field_order = [
        "project",
        "work_order",
        "name",
    ]

    class Meta:
        model = WorkEntry
        fields = "__all__"
        exclude = ['is_approved', 'docs', 'hourly_rate']
        widgets = {
            # sensible defaults; unknown keys are ignored by Django
            "notes": forms.Textarea(attrs={"rows": 3}),
            "date_time_in": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "date_time_out": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "period": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        # capture initial passed by the view so we can hide the user field
        initial = kwargs.get("initial", {})
        super().__init__(*args, **kwargs)

        # Apply a common CSS class to all widgets (e.g., for Bootstrap)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            classes = (existing + " form-control").strip()
            field.widget.attrs["class"] = classes

        # If the form was given an initial 'user', hide the user field from the UI
        # (it will still be submitted via the initial value or set in the view)
        # and populate alternate wage code choices for that user
        print("Initial in WorkEntryForm:", initial)
        if "user" in initial and "user" in self.fields:
            self.fields["user"].widget = forms.HiddenInput()
            # Populate alternate wage code choices for that user
            user = initial["user"]
            self.fields["alternate_wage_code"].queryset = AlternateWageCode.objects.filter(user=user)
        

    def clean(self):
        cleaned = super().clean()
        # Add cross-field validation here if needed (example placeholder)
        return cleaned


class WorkEntryInlineForm(WorkEntryForm):
    """Inline form used on the WorkOrder detail page.

    This excludes the `work_order` FK so the view binds the new entry to the
    current WorkOrder automatically.
    """

    class Meta(WorkEntryForm.Meta):
        model = WorkEntry
        # Exclude the FK so the inline form can't change which work order the
        # entry belongs to.
        exclude = ("work_order",)