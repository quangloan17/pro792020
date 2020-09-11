from django.urls import path
from .models import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('customer-debt', views.CustomerDebt.as_view(), name='customer-debt'),
    path('max-total', views.Index.as_view(ordering=['-receipt__deposit']), name='index-max-total'),
    path('customer-type', views.Index.as_view(ordering=['-customer_type']), name='customer-type'),
    path('customer-date', views.Index.as_view(ordering=['-create_date']), name='customer-date'),

    path('customer/', views.customers, name='customer'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('filter/', views.FilterView.as_view(), name='filter'),
    path('update/<int:pk>', views.UpdateView.as_view(), name='update'),
    path('read/<int:pk>', views.ReadView.as_view(), name='read'),
    path('delete/<int:pk>', views.DeleteView.as_view(), name='delete'),
    
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('customer-done/<id>', views.customer_done, name='customer-done'),

# Đăng nhập
	path('accounts/login/',auth_views.LoginView.as_view(template_name="login.html"), name="login-acc"),
	path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),

]