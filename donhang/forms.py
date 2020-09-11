from django import forms
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from khachhang.models import *
from django.forms import ModelForm, Textarea


class DonHangForm(BSModalModelForm):
    #Điều chỉnh nội dung trường thông tin bằng queryset
    def __init__(self, *args, **kwargs):
        super(DonHangForm, self).__init__(*args, **kwargs)
        self.fields['receipt'].queryset = Receipt.objects.filter(create_date__month = timezone.datetime.today().month).filter(approved_status = False).order_by('-create_date')
        self.fields['unit'].initial = 'Trang'

        
    #Điều chỉnh widget
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'popular_info': Textarea(attrs={'cols': 80, 'rows': 5}),

        }
        exclude = ['search_date','end_date','popular_info']
        
class VideoForm(BSModalModelForm):
    #Điều chỉnh nội dung trường thông tin bằng queryset
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['receipt'].queryset = Receipt.objects.filter(create_date__month = timezone.datetime.today().month).filter(approved_status = False).order_by('-create_date')
        self.fields['name'].initial = 'Dịch video'
        self.fields['order_type'].initial = 'Dịch video'
        self.fields['quantity'].initial = '1'
        self.fields['unit'].initial = 'Phút'
        self.fields['price'].initial = '40000'
    class Meta:
        model = Order
        fields = ['receipt','order_type', 'name','quantity', 'unit', 'price']


class ShipForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(ShipForm, self).__init__(*args, **kwargs)
        self.fields['receipt'].queryset = Receipt.objects.filter(create_date__month = timezone.datetime.today().month).filter(approved_status = False).order_by('-create_date')
        self.fields['order_type'].initial = 'Ship'
        self.fields['name'].initial = 'Ship'
        self.fields['quantity'].initial = '1'
        self.fields['unit'].initial = 'Lần'
        self.fields['price'].initial = '30000'
    
    class Meta:
        model = Order
        fields = ['receipt','order_type', 'name','quantity', 'unit', 'price']

class VatForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(VatForm, self).__init__(*args, **kwargs)
        self.fields['receipt'].queryset = Receipt.objects.filter(create_date__month = timezone.datetime.today().month).filter(approved_status = False).order_by('-create_date')
        self.fields['order_type'].initial = 'VAT'
        self.fields['name'].initial = 'VAT'
        self.fields['quantity'].initial = '1'
        self.fields['unit'].initial = 'Lần'
        self.fields['price'].initial = '100000'
    
    class Meta:
        model = Order
        fields = ['receipt','order_type', 'name','quantity', 'unit', 'price']