from django import forms
from .models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'series', 'price', 'rarity', 'clan', 'stock', 'image']
        labels = {
            'name': 'ชื่อการ์ด',
            'series': 'ชุดการ์ด (Series)',
            'price': 'ราคา (บาท)',
            'rarity': 'ความหายาก',
            'clan': 'คลาน/เนชั่น',
            'stock': 'จำนวนสต็อก',
            'image': 'รูปภาพการ์ด',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ชื่อการ์ด',
                'required': True
            }),
            'series': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ชุดการ์ด',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'rarity': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'RRR/RR/SP/R/BT',
                'list': 'rarity-list'
            }),
            'clan': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'คลาน/เนชั่น',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError('ราคาต้องมากกว่า 0')
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError('จำนวนสต็อกต้องมากกว่า 0')
        return stock
