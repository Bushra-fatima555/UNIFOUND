
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
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter item name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Describe your item',
                    'rows': 4
                }
            ),

            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter location'
                }
            ),
        }


class ClaimForm(forms.ModelForm):

    lost_item = forms.ModelChoiceField(
        queryset=Item.objects.none(),
        required=True,
        empty_label="Select your lost item",
        label="Select your Lost Item"
    )

    class Meta:
        model = Claim
        fields = ['lost_item', 'claim_message']

        widgets = {
            'claim_message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Explain why this item belongs to you',
                    'rows': 4
                }
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields['lost_item'].queryset = Item.objects.filter(
                user=user,
                item_type='LOST',
                status='ACTIVE'
            ).order_by('-created_at')

        self.fields['lost_item'].widget.attrs.update({
            'class': 'form-control'
        })
