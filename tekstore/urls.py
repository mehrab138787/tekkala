from django.urls import path, include
from django.shortcuts import redirect
from . import views

# ریدایرکت برای /accounts/login/
def redirect_to_custom_login(request):
    return redirect('/login/')

urlpatterns = [
    # صفحه اصلی
    path('', views.home, name='home'),

    # محصولات
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/add_comment/', views.add_product_comment, name='add_product_comment'),
    path('products/<int:product_id>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),  # ✅ اضافه شد
    path('search/', views.product_search, name='product_search'),

    # ورود / ثبت‌نام
    path('auth/', views.auth_view, name='auth'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # پروفایل
    path('profile/', views.profile_view, name='profile'),
    path('account/', views.profile_view, name='account'),
    path('profile/edit_field/', views.profile_edit_field, name='profile_edit_field'),
    path('profile/edit_email/', views.profile_edit_field, name='profile_edit_field'),

    # سبد خرید
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='cart_add'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/<int:quantity>/', views.update_cart, name='update_cart'),

    # تسویه‌حساب
    path('checkout/', views.checkout_view, name='checkout'),

    # دسته‌بندی
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),

    # پشتیبانی و تیکت
    path('support/', views.support_view, name='support'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('ticket_list/', views.ticket_list, name='ticket_list'),

    # چت آنلاین (پشتیبانی)
    path('support/chat/', views.chat_online, name='chat_online'),

    # درخواست همکاری
    path('cooperation/', views.cooperation_request_view, name='cooperation_request'),

    # داشبورد کاربری
    path('dashboard/', views.user_dashboard, name='user_dashboard'),

    # چت ادمین
    path('admin-chat/', views.admin_chat_view, name='admin_chat_view'),
    path('admin-chat/<int:chat_id>/', views.admin_chat_detail, name='admin_chat_detail'),
    path('admin-chat/<int:chat_id>/delete/', views.admin_chat_delete, name='admin_chat_delete'),

    # مسیرهای پیش‌فرض احراز هویت Django
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', redirect_to_custom_login),  # ریدایرکت برای جلوگیری از خطا
]

