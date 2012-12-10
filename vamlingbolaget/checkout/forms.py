from django import forms
from models import Checkout

class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'fyll i : ' + str(k)

    class Meta:
        model = Checkout