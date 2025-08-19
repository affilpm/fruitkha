from django.urls import path
from . import views


urlpatterns = [
  
    path('checkout/', views.checkout, name='checkout'),
    path('add-address-checkout/', views.add_address_checkout, name='add_address_checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    
    path('orders/', views.orders, name='orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('retry-razorpay/', views.retry_razorpay, name="retry_razorpay"),
    path('request-item-cancellation/<int:item_id>/', views.request_item_cancellation, name='request_item_cancellation'),
    
    path('order-invoice/<int:order_id>/', views.generate_invoice, name='order_invoice'),
    
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
    
    
    
    path('wallet/', views.wallet, name='wallet'),
    path('save-order/', views.save_order, name='save_order'),
    
    
    path('razorpay/', views.razorpay_view, name='razorpay'),
    path('payment-success/', views.success, name='payment_success'),
    
    
]
