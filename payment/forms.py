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


class PaymentForm(forms.Form):
    cart_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name On Cart"}),
        required=True,
    )
    cart_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Cart Number"}),
        required=True,
    )
    cart_exp_date = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Expiration Date"}),
        required=True,
    )
    cart_cvv_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "CVV Code"}),
        required=True,
    )
    cart_address1 =forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Billing Address 1"}),
        required=True,
    )
    cart_address2 =forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Billing Address 2"}),
        required=False,
    )
    cart_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Billing City"}),
        required=True,
    )
    cart_zipcode =forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Billing Zipcode"}),
        required=True,
    )
    cart_country =forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Billing Country"}),
        required=True,
    )

