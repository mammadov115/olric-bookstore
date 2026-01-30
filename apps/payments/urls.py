from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/<str:order_number>/', views.payment_process, name='process'),
    path('mock-gateway/<str:transaction_id>/', views.mock_gateway, name='mock_gateway'),
    path('callback/', views.payment_callback, name='callback'),
]
