# orders/urls.py
from django.urls import path
from accounts import views as account_views
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/<int:order_id>/', views.order_payment, name='order_payment'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('contact/', account_views.contact_view, name='contact'),
]