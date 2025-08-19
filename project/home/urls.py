from django.urls import path
from . import views


urlpatterns = [
    # User
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('customer-service/', views.customer_service, name='customer_service'),

    path('user-login/', views.user_login, name='user_login'),
    path('user-register/', views.user_register, name='user_register'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('otp/', views.otp, name='otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('delete-otp/', views.delete_otp, name='delete_otp'),
    
    
    path('single-product/<int:product_id>/', views.single_product, name='single_product'),
    
    
    path('address/', views.address, name='address'),
    path('address/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('add-address/', views.add_address, name='add_address'),
    
    
    path('user-profile/', views.user_profile, name='user_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('edit-username/', views.edit_username, name='edit_username'),
    path('edit-first-name/', views.edit_first_name, name='edit_first_name'),
    path('edit-last-name/', views.edit_last_name, name='edit_last_name'),
    
    
    # Admin
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout-admin/', views.logout_admin, name='logout_admin'),
    
    path('admin-dashboard/', views.admin_dashboard , name='admin_dashboard'),
    path('report/', views.report, name='report'),
    
    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('list_category/<int:category_id>/', views.list_category, name='list_category'),
    path('unlist_category/<int:category_id>/', views.unlist_category, name='unlist_category'),
    
    path('admin-product/', views.admin_product, name='admin_product'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('list-product/<int:product_id>/', views.list_product, name='list_product'),
    path('unlist-product/<int:product_id>/', views.unlist_product, name='unlist_product'),
    
    path('admin-users/', views.admin_users, name='admin_users'),
    path('search-users/', views.search_users, name='search_users'), 
    path('users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('users/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
   
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order-items/<int:order_id>', views.admin_order_items, name='admin_order_items'),
    path('admin-change-status/<int:item_id>/', views.admin_change_order_status, name='admin_change_order_status'),
    
    path('review-cancellation-requests/', views.review_cancellation_requests, name='review_cancellation_requests'),
    path('approve-cancellation-requests/<int:request_id>/', views.approve_cancellation_request, name='approve_cancellation_request'),
    
    path('admin-coupons/', views.admin_coupons, name='admin_coupons'),
    path('add-coupon', views.add_coupon, name='add_coupon'),
    path('admin-coupons/edit/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('admin-coupons/delete/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
        
    path('admin-offers/', views.admin_offers, name='admin_offers'),
    path('add-offer/', views.add_offer, name='add_offer'),
    path('edit-offer/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('offers/delete/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    
    # path('sales_report/', views.sales_report, name='sales_report'),
    # path('sales/', views.sales, name='sales'),
    
]
