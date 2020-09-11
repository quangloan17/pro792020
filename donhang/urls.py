from django.urls import path
from .models import *
from . import views
from .forms import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name='index-order'),
    path('create/<int:id>', views.CreateView.as_view(), name='create-order'),
    path('create-ship-order/<int:id>', views.CreateView.as_view(form_class = ShipForm), name='create-ship-order'),
    path('create-vat-order/<int:id>', views.CreateView.as_view(form_class = VatForm), name='create-vat-order'),
    path('create-video-order/<int:id>', views.CreateView.as_view(form_class = VideoForm), name='create-video-order'),
    path('create-orders/', views.OrdersCreateView.as_view(), name='create-orders'),
    path('create-ship-orders/', views.OrdersCreateView.as_view(form_class = ShipForm), name='create-ship-orders'),
    path('create-vat-orders/', views.OrdersCreateView.as_view(form_class = VatForm), name='create-vat-orders'),
    path('create-video-orders/', views.OrdersCreateView.as_view(form_class = VideoForm), name='create-video-orders'),
    path('orders-detail-list/<pk>', views.OrdersDetailView.as_view(), name='orders-detail-list'),
    path('update/<int:pk>', views.UpdateView.as_view(), name='update-order'),
    path('read/<int:pk>', views.ReadView.as_view(), name='read-order'),
    path('delete/<int:pk>', views.DeleteView.as_view(), name='delete-order'),
    path('orders/', views.orders, name='orders'),
]