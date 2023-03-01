from django import forms
from .models import MenuPoint


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuPoint
        fields = ('name', 'url', 'parent')