from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.detail import DetailView

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import *

from khachhang.models import *
from django.db.models import Q
import math

from django.shortcuts import redirect,render,HttpResponse,get_object_or_404,reverse
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ReceiptSent(generic.ListView):
    model = Receipt
    context_object_name = 'receipts'
    template_name = 'receipt/index.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.model.objects.filter(send_status=True)
        return qs

@method_decorator(login_required, name='dispatch')
class Index(generic.ListView):
    model = Receipt
    context_object_name = 'receipts'
    template_name = 'receipt/index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.model.objects.filter(approved_status=False)
        if 'keyword' in self.request.GET:
            qs = self.model.objects.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword']))| Q(customer__name__contains=str(self.request.GET['keyword']))
                )
        if 'type' in self.request.GET:
            qs = qs.filter(receipt_type=str(self.request.GET['type']))
        return qs

    def get_context_data(self,**kwargs):    
        context = super().get_context_data(**kwargs)
        context['tongtien_phieuthu'] = sum(pt.tongtien_order() for pt in self.model.objects.all())
        context['tongso'] = self.model.objects.all().count()
        context['tongtien_phaithu'] = sum(pt.phaithu() for pt in self.model.objects.all().filter(approved_status=False))
        context['tongtien_oxacnhan'] = sum(pt.tongtien_order() for pt in self.model.objects.all().filter(status=False))
        #Cần tối ưu cái này
        context['tongtien_dathu'] = sum(pt.deposit for pt in self.model.objects.all())

        context['tongso_dh_xacnhan'] = self.model.objects.all().filter(status=True).count()
        context['tongso_dh_datra'] = self.model.objects.all().filter(send_status=True).count()
        context['tongso_dh_thanhtoan'] = self.model.objects.all().filter(payment_status=True).count()

        context['tongso_dh_oxacnhan'] = self.model.objects.all().filter(status=False).count()
        context['tongso_dh_otra'] = self.model.objects.all().filter(send_status=False).count()
        context['tongso_dh_othanhtoan'] = self.model.objects.all().filter(payment_status=False).count()

        context['day'] = str(timezone.datetime.today().day)
        context['month'] = str(timezone.datetime.today().month)
        context['year'] = str(timezone.datetime.today().year)
        if 'keyword' in self.request.GET:
            context['keyword'] = str(self.request.GET['keyword'])
            qs = self.model.objects.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword']))| Q(customer__name__contains=str(self.request.GET['keyword']))
                )
            context['tongso'] = qs.count()
            context['tongtien_phieuthu'] = sum(qs.tongtien_order() for qs in qs)
            context['tongtien_phaithu'] = sum(qs.phaithu() for qs in qs)
            context['tongtien_oxacnhan'] = sum(pt.tongtien_order() for pt in qs.filter(status=False))
            context['tongtien_dathu'] = sum(pt.deposit for pt in qs)

            context['tongso_dh_xacnhan'] = qs.filter(status=True).count()
            context['tongso_dh_datra'] = qs.filter(send_status=True).count()
            context['tongso_dh_thanhtoan'] = qs.filter(payment_status=True).count()

            context['tongso_dh_oxacnhan'] = qs.filter(status=False).count()
            context['tongso_dh_otra'] = qs.filter(send_status=False).count()
            context['tongso_dh_othanhtoan'] = qs.filter(payment_status=False).count()
        return context

#Tạo phiếu thu không cần id
@method_decorator(login_required, name='dispatch')
class ReceiptsCreateView(BSModalCreateView):
    model = Receipt
    template_name = 'receipt/create.html'
    form_class = PhieuThuForm
    success_url = reverse_lazy('index-receipt')


#Tạo phiếu thu bắt qua id đơn hàng
@method_decorator(login_required, name='dispatch')
class CreateView(BSModalCreateView):
    model = Receipt
    template_name = 'receipt/create.html'
    form_class = PhieuThuForm

    def get_initial(self, *args, **kwargs):
        initial = super(CreateView, self).get_initial(**kwargs)
        initial['customer'] = self.kwargs['id']
        return initial

    def get_success_url(self):
        return reverse('receipts-detail-list', kwargs={'pk': self.kwargs['id']})


#Xem chi tiết phiếu thu
@method_decorator(login_required, name='dispatch')
class ReceiptsDetailView(generic.ListView):
    model = Receipt
    template_name = 'receipt/_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiptsDetailView,self).get_context_data(**kwargs)
        customer = Customer.objects.get(id=self.kwargs['pk'])
        if 'keyword' in self.request.GET:
            context['keyword'] = str(self.request.GET['keyword'])
            qs = self.model.objects.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword'])) | Q(customer__name__contains=str(self.request.GET['keyword']))
                )
        
            customer_list_receipts = customer.receipt_set.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword'])) 
                )
            total_customer_list_receipts = sum(receipt.deposit for receipt in qs)
            context['customer'] = customer
            context['receipts'] = customer_list_receipts
            context['total_customer_list_receipts'] = total_customer_list_receipts
        else:
            customer_list_receipts = customer.receipt_set.all()
            total_customer_list_receipts = sum(receipt.deposit for receipt in customer_list_receipts)
            context['customer'] = customer
            context['receipts'] = customer_list_receipts
            context['total_customer_list_receipts'] = total_customer_list_receipts
        context['day'] = str(timezone.datetime.today().day)
        context['month'] = str(timezone.datetime.today().month)
        context['year'] = str(timezone.datetime.today().year)   
        return context

@method_decorator(login_required, name='dispatch')
class UpdateView(BSModalUpdateView):
    model = Receipt
    template_name = 'receipt/update.html'
    form_class = PhieuThuForm
    success_message = 'Success: Updated.'
    success_url = reverse_lazy('index-receipt')

@method_decorator(login_required, name='dispatch')
class ReadView(BSModalReadView):
    model = Receipt
    template_name = 'receipt/read.html'

@method_decorator(login_required, name='dispatch')
class DeleteView(BSModalDeleteView):
    model = Receipt
    template_name = 'receipt/delete.html'
    success_message = 'Success: Deleted.'
    success_url = reverse_lazy('index-receipt')


@login_required
def receipts(request):
    data = dict()
    if request.method == 'GET':
        receipts = Receipt.objects.all()
        data['table'] = render_to_string(
            'receipt/_all_table.html',
            {'receipts': receipts},
            request=request
        )
        return JsonResponse(data)
    
    
def confirm_receipt(request,id):
    data = Receipt.objects.get(pk=id)
    id = data.id
    data.status = True
    data.save()
    return redirect('index-receipt')


def send_receipt(request,id):
    data = Receipt.objects.get(pk=id)
    id = data.id
    data.send_status = True
    data.save()
    return redirect('index-receipt')


def paid_receipt(request,id):
    data = Receipt.objects.get(pk=id)
    id = data.id
    data.payment_status = True
    data.deposit = data.tongtien_order()
    data.save()
    return redirect('index-receipt')


def approved_receipt(request,id):
    data = Receipt.objects.get(pk=id)
    id = data.id
    data.approved_status = True
    data.save()
    return redirect('index-receipt')