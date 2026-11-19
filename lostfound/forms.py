from django import forms
from .models import Item, Claim


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = [
            'item_name',
            'item_type',
            'category',
            'description',
            'date',
            'location',
            'image',
        ]

        widgets = {
            'item_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter item name'}
            ),

            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Describe your item',
                       'rows': 4}
            ),

            'date': forms.DateInput(
                attrs={'type': 'date',
                       'class': 'form-control'}
            ),

            'location': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter location'}
            ),
        }


class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        fields = ['claim_message']

        widgets = {
            'claim_message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Explain why this item belongs to you',
                    'rows': 4
                }
            )
        }