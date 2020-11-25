from django.urls import path
from .import views

app_name = 'gateway'

urlpatterns = [
    path('checkout/<int:id>/', views.checkout_page, name='checkout'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('purchase_success/', views.success, name='purchase_success'),
    path('purchase_cancel/',views.cancel, name='purchase_cancel')
]