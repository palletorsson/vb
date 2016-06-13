from django import forms
from models import Checkout

LANG = (
    ('Sverige', 'Sverige'),
    ('Finland', 'Suomi'),
    ('Tyskland', 'Deutschland'),
    ('Danmark', 'Danmark'),
    ('Norge', 'Norge'),
    ('Other', 'Other'),
)

class CheckoutForm(forms.ModelForm):
    country = forms.ChoiceField(choices=LANG)


    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'fyll i : ' + str(k)

    class Meta:
        model = Checkout