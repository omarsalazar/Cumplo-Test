from django import forms

CURRENCIES = [
    ('UDI', 'UDI'),
    ('USD', 'USD'),
    ('TIIE', 'TIIE'),
]


class CurrencyForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    currency = forms.CharField(
        widget=forms.Select(choices=CURRENCIES)
    )
