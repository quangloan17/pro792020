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
class Index(generic.ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'keyword' in self.request.GET:
            qs = self.model.objects.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword'])) | Q(order_type__contains=str(self.request.GET['keyword'])) | Q(language_type__contains=str(self.request.GET['keyword']))
                )
        if 'type' in self.request.GET:
            qs = qs.filter(order_type=str(self.request.GET['type']))
        return qs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if 'keyword' in self.request.GET:
            context['keyword'] = str(self.request.GET['keyword'])
            qs = self.model.objects.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword'])) | Q(order_type__contains=str(self.request.GET['keyword'])) | Q(language_type__contains=str(self.request.GET['keyword']))
                )
            context['tongso'] = qs.count()
            context['orders_total'] = sum(dh.tongtien() for dh in qs)
            
            context['orders_english'] = sum(dh.tongtien() for dh in qs.filter(language_type="Tiếng Anh"))
            context['orders_english_qty'] = qs.filter(language_type="Tiếng Anh").count()
            context['orders_china'] = sum(dh.tongtien() for dh in qs.filter(language_type="Tiếng Trung"))
            context['orders_china_qty'] = qs.filter(language_type="Tiếng Trung").count()
            context['orders_japan'] = sum(dh.tongtien() for dh in qs.filter(language_type="Tiếng Nhật"))
            context['orders_japan_qty'] = qs.filter(language_type="Tiếng Nhật").count()
            context['orders_korea'] = sum(dh.tongtien() for dh in qs.filter(language_type="Tiếng Hàn"))
            context['orders_korea_qty'] = qs.filter(language_type="Tiếng Hàn").count()
            context['orders_france'] = sum(dh.tongtien() for dh in qs.filter(language_type="Tiếng Pháp"))
            context['orders_france_qty'] = qs.filter(language_type="Tiếng Pháp").count()
            context['orders_germany'] = sum(dh.tongtien() for dh in qs.filter(language_type="Tiếng Đức"))
            context['orders_germany_qty'] = qs.filter(language_type="Tiếng Đức").count()
            context['orders_russia'] = sum(dh.tongtien() for dh in qs.filter(language_type="Tiếng Nga"))
            context['orders_russia_qty'] = qs.filter(language_type="Tiếng Nga").count()
            context['orders_dt'] = sum(dh.tongtien() for dh in qs.filter(order_type="Dịch thuật"))
            context['orders_dt_qty'] = qs.filter(order_type="Dịch thuật").count()
            context['orders_saoy'] = sum(dh.tongtien() for dh in qs.filter(order_type="Sao y"))
            context['orders_saoy_qty'] = qs.filter(order_type="Sao y").count()
            context['orders_cc'] = sum(dh.tongtien() for dh in qs.filter(order_type="Công chứng"))
            context['orders_cc_qty'] = qs.filter(order_type="Công chứng").count()
            context['orders_ship'] = sum(dh.tongtien() for dh in qs.filter(order_type="Ship"))
            context['orders_ship_qty'] = qs.filter(order_type="Ship").count()
        else:
            context['tongso'] = self.model.objects.all().count()
            context['orders_total'] = sum(dh.tongtien() for dh in self.model.objects.all())
            context['orders_english'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(language_type="Tiếng Anh"))
            context['orders_english_qty'] = self.model.objects.all().filter(language_type="Tiếng Anh").count()
            context['orders_china'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(language_type="Tiếng Trung"))
            context['orders_china_qty'] = self.model.objects.all().filter(language_type="Tiếng Trung").count()
            context['orders_japan'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(language_type="Tiếng Nhật"))
            context['orders_japan_qty'] = self.model.objects.all().filter(language_type="Tiếng Nhật").count()
            context['orders_korea'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(language_type="Tiếng Hàn"))
            context['orders_korea_qty'] = self.model.objects.all().filter(language_type="Tiếng Hàn").count()
            context['orders_france'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(language_type="Tiếng Pháp"))
            context['orders_france_qty'] = self.model.objects.all().filter(language_type="Tiếng Pháp").count()
            context['orders_germany'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(language_type="Tiếng Đức"))
            context['orders_germany_qty'] = self.model.objects.all().filter(language_type="Tiếng Đức").count()
            context['orders_russia'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(language_type="Tiếng Nga"))
            context['orders_russia_qty'] = self.model.objects.all().filter(language_type="Tiếng Nga").count()
            context['orders_dt'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(order_type="Dịch thuật"))
            context['orders_dt_qty'] = self.model.objects.all().filter(order_type="Dịch thuật").count()
            context['orders_saoy'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(order_type="Sao y"))
            context['orders_saoy_qty'] = self.model.objects.all().filter(order_type="Sao y").count()
            context['orders_cc'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(order_type="Công chứng"))
            context['orders_cc_qty'] = self.model.objects.all().filter(order_type="Công chứng").count()
            context['orders_ship'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(order_type="Ship"))
            context['orders_ship_qty'] = self.model.objects.all().filter(order_type="Ship").count()
        context['tongso_month'] = self.model.objects.all().filter(create_date__month = timezone.datetime.today().month).count()
        context['orders_total_month'] = sum(dh.tongtien() for dh in self.model.objects.all().filter(create_date__month= timezone.datetime.today().month))
        context['day'] = str(timezone.datetime.today().day)
        context['month'] = str(timezone.datetime.today().month)
        context['year'] = str(timezone.datetime.today().year)
        return context

#Tạo phiếu thu không cần id
@method_decorator(login_required, name='dispatch')
class OrdersCreateView(BSModalCreateView):
    model = Order
    template_name = 'order/create.html'
    form_class = DonHangForm
    success_url = reverse_lazy('index-order')

#Tạo phiếu thu bắt qua id đơn hàng
@method_decorator(login_required, name='dispatch')
class CreateView(BSModalCreateView):
    model = Order
    template_name = 'order/create.html'
    form_class = DonHangForm
    
    def get_initial(self, *args, **kwargs):
        initial = super(CreateView, self).get_initial(**kwargs)
        initial['receipt'] = self.kwargs['id']
        return initial

    def get_success_url(self):
        return reverse('orders-detail-list', kwargs={'pk': self.kwargs['id']})


#Xem chi tiết phiếu thu
@method_decorator(login_required, name='dispatch')
class OrdersDetailView(generic.ListView):
    model = Order
    template_name = 'order/_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersDetailView,self).get_context_data(**kwargs)
            
        receipt = Receipt.objects.get(id=self.kwargs['pk'])
        if 'keyword' in self.request.GET:
            context['keyword'] = str(self.request.GET['keyword'])
            receipt_list_orders = receipt.order_set.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword']))
                )
            context['receipt'] = receipt
            context['orders'] = receipt_list_orders
        else:
            receipt_list_orders = receipt.order_set.all()
            context['receipt'] = receipt
            context['orders'] = receipt_list_orders
        context['orders_amount'] = sum(dh.tongtien() for dh in receipt_list_orders)
        context['day'] = str(timezone.datetime.today().day)
        context['month'] = str(timezone.datetime.today().month)
        context['year'] = str(timezone.datetime.today().year)   
        
        return context

@method_decorator(login_required, name='dispatch')
class UpdateView(BSModalUpdateView):
    model = Order
    template_name = 'order/update.html'
    form_class = DonHangForm
    success_message = 'Success: Updated.'
    success_url = reverse_lazy('index-order')

@method_decorator(login_required, name='dispatch')
class ReadView(BSModalReadView):
    model = Order
    template_name = 'order/read.html'

@method_decorator(login_required, name='dispatch')
class DeleteView(BSModalDeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_message = 'Success: Deleted.'
    success_url = reverse_lazy('index-order')


@login_required
def orders(request):
    data = dict()
    if request.method == 'GET':
        orders = Order.objects.all()
        data['table'] = render_to_string(
            'order/_all_table.html',
            {'orders': orders},
            request=request
        )
        return JsonResponse(data)
