from django import forms
from useradmin.models import Medicine

class MedicineForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        )
    type = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        )
    details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=500,
        required=True,
    )
    class Meta:
        model = Medicine
        fields = ['name', 'type', 'details']