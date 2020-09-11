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

from .forms import (
    KhachHangForm,
    FilterForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
)
from .models import *
from django.db.models import Q
import math

from django.shortcuts import redirect,render,HttpResponse
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class CustomerDebt(generic.ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'index.html'
    ordering = ['-create_date']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Customer.objects.filter(receipt__payment_status=False)
        return qs


@method_decorator(login_required, name='dispatch')
class Index(generic.ListView):
    model = Customer
    paginate_by = 5
    context_object_name = 'customers'
    template_name = 'index.html'
    ordering = ['-create_date']
    
    customer_this_month = model.objects.filter(create_date__month = timezone.datetime.today().month)
    customer_all = model.objects.all()
    customer_north = model.objects.filter(city = "Miền Bắc")
    customer_south = model.objects.filter(city = "Miền Nam")
    customer_central = model.objects.filter(city = "Miền Trung")
    customer_other = model.objects.filter(city = "Khác")
    customer_kle = model.objects.filter(customer_type = "Khách lẻ")
    customer_kthang = model.objects.filter(customer_type = "Khách tháng")
    customer_idt = model.objects.filter(customer_type__icontains = "IDT")
    customer_khac = model.objects.filter(customer_type = "Khác")

    def get_queryset(self):
        qs = super().get_queryset()
        if 'keyword' in self.request.GET:
            qs = self.model.objects.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword'])) | Q(popular_info__contains=str(self.request.GET['keyword'])) 
                )
        if 'type' in self.request.GET:
            qs = qs.filter(customer_type=str(self.request.GET['type']))
        return qs

    def get_context_data(self,**kwargs):    
        context = super().get_context_data(**kwargs)
        if 'keyword' in self.request.GET:
            context['keyword'] = self.request.GET['keyword']
            qs = self.model.objects.filter(
                Q(search_date__contains=str(self.request.GET['keyword'])) | Q(name__contains=str(self.request.GET['keyword'])) | Q(popular_info__contains=str(self.request.GET['keyword'])) 
                )
                
            context['tongso'] = qs.count()
            context['customer_north'] = qs.filter(city = "Miền Bắc").count()
            context['customer_south'] = qs.filter(city = "Miền Nam").count()
            context['customer_central'] = qs.filter(city = "Miền Trung").count()
            context['customer_other'] = qs.filter(city = "Khác").count()
            context['customer_kle'] = qs.filter(customer_type__icontains = "Khách lẻ").count()
            context['customer_kthang'] = qs.filter(customer_type__icontains = "Khách tháng").count()
            context['customer_idt'] = qs.filter(customer_type__icontains = "IDT").count()
            context['customer_khac'] = qs.filter(customer_type = "Khác").count()

            context['customer_north_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(city = "Miền Bắc"))
            context['customer_south_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(city = "Miền Nam"))
            context['customer_central_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(city = "Miền Trung"))
            context['customer_other_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(city = "Khác"))
            context['customer_kle_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(customer_type__icontains = "Khách lẻ"))
            context['customer_kthang_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(customer_type__icontains = "Khách tháng"))
            context['customer_idt_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(customer_type__icontains = "IDT"))
            context['customer_khac_total'] = sum(qs.tongtien_receipt() for qs in qs.filter(customer_type = "Khác"))
        else:
            context['tongso'] = self.customer_all.count()
            context['customer_north'] = self.customer_north.count()
            context['customer_south'] = self.customer_south.count()
            context['customer_central'] = self.customer_central.count()
            context['customer_other'] = self.customer_other.count()
            context['customer_kle'] = self.customer_kle.count()
            context['customer_kthang'] = self.customer_kthang.count()
            context['customer_idt'] = self.customer_idt.count()
            context['customer_khac'] = self.customer_khac.count()
            
            context['customer_north_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(city = "Miền Bắc"))
            context['customer_south_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(city = "Miền Nam"))
            context['customer_central_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(city = "Miền Trung"))
            context['customer_other_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(city = "Khác"))
            context['customer_kle_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(customer_type__icontains = "Khách lẻ"))
            context['customer_kthang_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(customer_type__icontains = "Khách tháng"))
            context['customer_idt_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(customer_type__icontains = "IDT"))
            context['customer_khac_total'] = sum(qs.tongtien_receipt() for qs in self.customer_all.filter(customer_type = "Khác"))
        
        context['day'] = str(timezone.datetime.today().day)
        context['month'] = str(timezone.datetime.today().month)
        context['year'] = str(timezone.datetime.today().year) 
        return context

@method_decorator(login_required, name='dispatch')
class FilterView(BSModalFormView):
    template_name = 'customer/filter.html'
    form_class = FilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        elif 'type' in self.request.POST:
            self.filter = '?type=' + form.cleaned_data['type']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('index') + self.filter


@method_decorator(login_required, name='dispatch')
class CreateView(BSModalCreateView):
    model = Customer
    template_name = 'customer/create.html'
    form_class = KhachHangForm
    # success_message = 'Success: Created.'
    success_url = reverse_lazy('index')
    
    def get_initial(self, *args, **kwargs):
        initial = super(CreateView, self).get_initial(**kwargs)
        initial['name'] = 'Tên gợi nhớ'
        initial['popular_info'] = '- Tên KH: \n- Địa chỉ: \n- MST: '
        initial['private_info'] = '- Người liên hệ: \n- Email: \n- Số ĐT: \n- Ngôn ngữ dịch: \n- Giá dịch: \n- Giá công chứng: \n- Giá sao y: \n- Làm gấp: \n- Khác: \n- Người liên hệ: \n- Email: \n- Số ĐT: \n- Ngôn ngữ dịch: \n- Giá dịch: '
        return initial

@method_decorator(login_required, name='dispatch')
class UpdateView(BSModalUpdateView):
    model = Customer
    template_name = 'customer/update.html'
    form_class = KhachHangForm
    success_message = 'Success: Updated.'
    success_url = reverse_lazy('index')

@method_decorator(login_required, name='dispatch')
class ReadView(BSModalReadView):
    model = Customer
    template_name = 'customer/read.html'

@method_decorator(login_required, name='dispatch')
class DeleteView(BSModalDeleteView):
    model = Customer
    template_name = 'customer/delete.html'
    success_message = 'Success: Deleted.'
    success_url = reverse_lazy('index')


@method_decorator(login_required, name='dispatch')
class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'customer/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')
    
@method_decorator(login_required, name='dispatch')
class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'customer/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index')



@login_required
def customer_done(request,id):
    data = Customer.objects.get(pk=id)
    id = data.id
    data.status = 'True'
    data.save()
    return redirect('index')

@login_required
def customers(request):
    data = dict()
    if request.method == 'GET':
        customers = Customer.objects.all()
        data['table'] = render_to_string(
            '_all_table.html',
            {'customers': customers},
            request=request
        )
        return JsonResponse(data)
