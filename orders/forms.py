from django import forms
from django.contrib.auth import get_user_model

from .models import UserAddress, ADDRESS_TYPE

User = get_user_model()


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField(label='Confirm Email')

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")

        if email == email2:
            user_exists = User.objects.filter(email=email).count()
            if user_exists != 0:
                raise forms.ValidationError("This User already exists Please login Instead.")
            return email2
        else:
            raise forms.ValidationError("Emails doesn't match.")


class AddressForm(forms.Form):
    billing_address = forms.ModelChoiceField(
            queryset=UserAddress.objects.filter(type="billing"),
            empty_label=None,
            widget=forms.RadioSelect,
    )
    shipping_address = forms.ModelChoiceField(
            queryset=UserAddress.objects.filter(type="shipping"),
            empty_label=None,
            widget=forms.RadioSelect,
    )


class UserAddressForm(forms.ModelForm):
    type = forms.ChoiceField(choices=ADDRESS_TYPE)

    class Meta:
        model = UserAddress

        fields = [
            'street',
            'city',
            'state',
            'zipcode',
            'type',
        ]
