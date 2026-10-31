from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "phone", "email",
                  "delivery", "city", "address", "payment", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
            "phone": forms.TextInput(attrs={"placeholder": "+380…", "type": "tel"}),
            "address": forms.TextInput(attrs={"placeholder": "№ відділення або вулиця, будинок"}),
        }
