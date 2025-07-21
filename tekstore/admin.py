
from django.contrib import admin
from .models import Product, Cart, CartItem, Ticket, TicketComment, CooperationRequest, Category, Profile

# Inline کامنت‌های تیکت
class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1

# پنل ادمین تیکت‌ها
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user', 'is_resolved', 'created_at', 'updated_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('subject', 'message')
    inlines = [TicketCommentInline]

    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f"{updated} تیکت به عنوان حل شده علامت گذاری شدند.")
    mark_as_resolved.short_description = "علامت گذاری تیکت‌ها به عنوان حل شده"

# پنل ادمین کامنت‌های تیکت‌ها
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'message', 'created_at')
    list_filter = ('created_at',)

# پنل ادمین محصولات
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at')
    list_filter = ('created_at', 'price')
    search_fields = ('title',)
    date_hierarchy = 'created_at'  # فیلتر براساس تاریخ

# پنل ادمین سبد خرید
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)

# پنل ادمین آیتم‌های سبد خرید
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')

# پنل ادمین درخواست همکاری
class CooperationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'products', 'is_reviewed', 'submitted_at')
    list_filter = ('is_reviewed', 'submitted_at')
    search_fields = ('phone', 'products')
    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(is_reviewed=True)
        self.message_user(request, f"{updated} درخواست همکاری بررسی شد.")
    mark_as_reviewed.short_description = "علامت گذاری درخواست‌های همکاری به عنوان بررسی شده"

# پنل ادمین دسته‌بندی
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

# پنل ادمین پروفایل
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'image')
    search_fields = ('user__username', 'phone')

# ثبت مدل‌ها در ادمین
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)
admin.site.register(CooperationRequest, CooperationRequestAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
