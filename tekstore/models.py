from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ✅ مدل پروفایل کاربر
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='شماره تماس')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name='عکس پروفایل')

    def __str__(self):
        return f"پروفایل {self.user.username}"

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربران'


# ✅ مدل دسته‌بندی
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام دسته‌بندی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات دسته‌بندی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'


# ✅ مدل محصول
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان محصول')
    description = models.TextField(verbose_name='توضیحات محصول')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='تصویر محصول')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='دسته‌بندی')

    def __str__(self):
        return self.title


# ✅ مدل نظرات محصول
class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    text = models.TextField(verbose_name='نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')

    def __str__(self):
        return f"نظر برای {self.product.title} از {self.user.username}"
    
    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصولات'


# ✅ مدل سبد خرید
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f"سبد خرید {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


# ✅ مدل آیتم سبد خرید
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    def __str__(self):
        return f"{self.quantity} × {self.product.title}"

    def total_price(self):
        return self.product.price * self.quantity


# ✅ مدل سفارش
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    items = models.ManyToManyField(CartItem, verbose_name='محصولات سفارش داده‌شده')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت کل')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت سفارش')
    status = models.CharField(max_length=20, default='در حال بررسی', verbose_name='وضعیت سفارش')

    def __str__(self):
        return f"سفارش #{self.id} - {self.user.username}"


# ✅ مدل تیکت پشتیبانی
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', verbose_name='کاربر')
    subject = models.CharField(max_length=255, verbose_name='موضوع تیکت')
    message = models.TextField(verbose_name='پیام تیکت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='زمان آخرین بروزرسانی')
    is_resolved = models.BooleanField(default=False, verbose_name='حل شده؟')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان حل شدن تیکت')

    def __str__(self):
        return f"تیکت #{self.id} - {self.subject}"


# ✅ مدل پاسخ به تیکت
class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments', verbose_name='تیکت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')

    def __str__(self):
        return f"پاسخ به تیکت #{self.ticket.id} - {self.user.username}"


# ✅ مدل درخواست همکاری
class CooperationRequest(models.Model):
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    products = models.CharField(max_length=255, verbose_name='محصولات ارائه شده')
    details = models.TextField(verbose_name='توضیحات تکمیلی')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')
    is_reviewed = models.BooleanField(default=False, verbose_name='بررسی شده؟')

    def __str__(self):
        return f"درخواست همکاری از شماره {self.phone}"


# ✅ مدل‌های چت و پیام‌ها
class Chat(models.Model):
    participants = models.ManyToManyField(User, verbose_name='شرکت‌کنندگان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f"چت #{self.id} - {'، '.join(p.username for p in self.participants.all())}"

    class Meta:
        verbose_name = 'چت'
        verbose_name_plural = 'چت‌ها'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name='چت')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فرستنده')
    content = models.TextField(verbose_name='متن پیام')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

    class Meta:
        verbose_name = 'پیام چت'
        verbose_name_plural = 'پیام‌های چت'
        ordering = ['timestamp']


# ✅ مدل علاقه‌مندی (Wishlist)
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by', verbose_name='محصول')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن')

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'علاقه‌مندی'
        verbose_name_plural = 'علاقه‌مندی‌ها'

    def __str__(self):
        return f"{self.user.username} → {self.product.title}"
