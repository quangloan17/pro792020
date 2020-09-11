from django.urls import path
from .models import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name='index-receipt'),
    path('sent-receipt', views.ReceiptSent.as_view(), name='sent-receipt'),

    path('create/<int:id>', views.CreateView.as_view(), name='create-receipt'),
    path('create-receipts/', views.ReceiptsCreateView.as_view(), name='create-receipts'),
    path('receipts-detail-list/<pk>', views.ReceiptsDetailView.as_view(), name='receipts-detail-list'),
    path('update/<int:pk>', views.UpdateView.as_view(), name='update-receipt'),
    path('read/<int:pk>', views.ReadView.as_view(), name='read-receipt'),
    path('delete/<int:pk>', views.DeleteView.as_view(), name='delete-receipt'),
    path('receipts/', views.receipts, name='receipts'),
    path('paid_receipts/<int:id>', views.paid_receipt, name='paid_receipt'),
    path('confirm_receipt/<int:id>', views.confirm_receipt, name='confirm_receipt'),
    path('send_receipt/<int:id>', views.send_receipt, name='send_receipt'),
    path('approved_receipt/<int:id>', views.approved_receipt, name='approved_receipt'),

]

