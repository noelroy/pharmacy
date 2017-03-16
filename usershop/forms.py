from django import forms
from usershop.models import ShopStock


class StockForm(forms.ModelForm):
    exp_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = ShopStock
        fields = ['medicine','exp_date','price','quantity']