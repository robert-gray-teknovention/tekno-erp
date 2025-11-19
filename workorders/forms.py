from django import forms
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
            "description": forms.Textarea(attrs={"rows": 2}),
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

            class Meta:
                model = WorkEntry
                fields = "__all__"
                widgets = {
                    # sensible defaults; unknown keys are ignored by Django
                    "description": forms.Textarea(attrs={"rows": 4}),
                    "notes": forms.Textarea(attrs={"rows": 3}),
                    "date": forms.DateInput(attrs={"type": "date"}),
                    "start_time": forms.TimeInput(attrs={"type": "time"}),
                    "end_time": forms.TimeInput(attrs={"type": "time"}),
                    "logged_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
                }

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                # Apply a common CSS class to all widgets (e.g., for Bootstrap)
                for field in self.fields.values():
                    existing = field.widget.attrs.get("class", "")
                    classes = (existing + " form-control").strip()
                    field.widget.attrs["class"] = classes

            def clean(self):
                cleaned = super().clean()
                # Add cross-field validation here if needed (example placeholder)
                return cleaned