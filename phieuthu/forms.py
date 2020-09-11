from django import forms
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from khachhang.models import *
from django.forms import ModelForm, Textarea


class PhieuThuForm(BSModalModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        widgets = {
            'popular_info': Textarea(attrs={'cols': 80, 'rows': 5}),
            'private_info': Textarea(attrs={'cols': 80, 'rows': 5}),

        }
        exclude = ['search_date','end_date','status','payment_status','send_status','approved_status']

    def __init__(self, *args, **kwargs):
        super(PhieuThuForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = self.fields['customer'].queryset.order_by('-create_date')


