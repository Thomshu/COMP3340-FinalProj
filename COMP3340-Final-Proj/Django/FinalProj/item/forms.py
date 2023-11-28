from django import forms
from django.forms.widgets import ClearableFileInput, CheckboxInput, TextInput
from .models import Item, Images


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'stock')

        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'stock')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
        }
