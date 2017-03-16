from django import forms
from usercompany.models import CompanyStock


class StockForm(forms.ModelForm):
    batch_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        )
    exp_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-control d-inline'}),
        required=True
    )

    class Meta:
        model = CompanyStock
        fields = ['batch_no', 'medicine','exp_date','price','quantity']