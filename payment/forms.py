from django import forms
from .models import ShipppingAddres


class ShippingForm(forms.ModelForm):

    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_full_name"}),
        required=False,
    )
    shipping_email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_email"}),
        required=False,
    )
    shipping_address1 = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "shipping_address1"}
        ),
        required=False,
    )
    shipping_address2 = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "shipping_address2"}
        ),
        required=False,
    )
    shipping_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_city"}),
        required=False,
    )
    shipping_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "shipping_zipcode"}
        ),
        required=False,
    )
    shipping_country = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "shipping_country"}
        ),
        required=False,
    )

    class Meta:
        model = ShipppingAddres
        fields = [
            "shipping_full_name",
            "shipping_email",
            "shipping_address1",
            "shipping_address2",
            "shipping_city",
            "shipping_zipcode",
            "shipping_country",
        ]
        exclude = ["user"]