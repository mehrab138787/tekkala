from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Ticket, Category, ProductComment, CooperationRequest, Chat, Message, Wishlist
from .forms import PersianSignUpForm, TicketForm
import json
from django.http import JsonResponse

# صفحه اصلی
def home(request):
    return render(request, 'tekstore/home.html')

# لیست محصولات
def product_list(request):
    products = Product.objects.all()
    return render(request, 'tekstore/product_list.html', {'products': products})

# جزئیات یک محصول خاص
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = product.comments.all()
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    return render(request, 'tekstore/product_detail.html', {
        'product': product,
        'comments': comments,
        'is_in_wishlist': is_in_wishlist
    })

# جستجوی محصول
def product_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(title__icontains=query)
    return render(request, 'tekstore/search_results.html', {'query': query, 'results': results})

# صفحه ورود و ثبت‌نام ترکیبی
def auth_view(request):
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            signup_form = PersianSignUpForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید.')
                return redirect('home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        elif 'signup_submit' in request.POST:
            signup_form = PersianSignUpForm(request.POST)
            login_form = AuthenticationForm()
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, 'ثبت‌نام با موفقیت انجام شد و وارد شدید.')
                return redirect('home')
            else:
                messages.error(request, 'لطفا خطاهای فرم ثبت‌نام را اصلاح کنید.')
    else:
        login_form = AuthenticationForm()
        signup_form = PersianSignUpForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, 'tekstore/auth.html', context)

# تابع ثبت‌نام
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد!')
            return redirect('login')
        else:
            messages.error(request, 'لطفا خطاهای فرم را اصلاح کنید.')
    else:
        form = UserCreationForm()
    return render(request, 'tekstore/register.html', {'form': form})

# تابع ورود
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید.')
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = AuthenticationForm()
    return render(request, 'tekstore/login.html', {'form': form})

# خروج
def logout_view(request):
    logout(request)
    messages.info(request, 'شما با موفقیت خارج شدید.')
    return redirect('auth')

# صفحه حساب کاربری
@login_required
def profile_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'tekstore/profile.html', {
        'user': request.user,
        'wishlist_items': wishlist_items
    })

# افزودن/حذف علاقه‌مندی
@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        messages.info(request, 'محصول از لیست علاقه‌مندی حذف شد.')
    else:
        messages.success(request, 'محصول به لیست علاقه‌مندی اضافه شد.')
    return redirect('product_detail', pk=pk)

# افزودن محصول به سبد خرید
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        cart[str(pk)] += 1
    else:
        cart[str(pk)] = 1
    request.session['cart'] = cart
    return redirect('cart_detail')

# نمایش سبد خرید
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for pk, qty in cart.items():
        product = get_object_or_404(Product, pk=pk)
        item_total = product.price * qty
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': item_total
        })
    return render(request, 'tekstore/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

# حذف محصول از سبد خرید
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('cart_detail')

# بروزرسانی تعداد محصول در سبد خرید
def update_cart(request, pk, qty):
    cart = request.session.get('cart', {})
    if str(pk) in cart and int(qty) > 0:
        cart[str(pk)] = int(qty)
        request.session['cart'] = cart
    return redirect('cart_detail')

# دسته‌بندی‌ها
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'tekstore/categories.html', {'categories': categories})

# جزئیات دسته‌بندی
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'tekstore/category_detail.html', {'category': category, 'products': products})

# پشتیبانی
def support_view(request):
    return render(request, 'tekstore/support.html')

# ارسال تیکت
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'تیکت شما با موفقیت ارسال شد.')
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tekstore/create_ticket.html', {'form': form})

# لیست تیکت‌ها
@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'tekstore/ticket_list.html', {'tickets': tickets})

# ویو تسویه حساب
@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for pk, qty in cart.items():
        product = get_object_or_404(Product, pk=pk)
        item_total = product.price * qty
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': item_total
        })
    return render(request, 'tekstore/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

# ویرایش ایمیل در پروفایل
@login_required
def profile_edit_field(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'ایمیل شما با موفقیت به‌روزرسانی شد.')
            return redirect('profile_view')
        else:
            messages.error(request, 'لطفا ایمیل را وارد کنید.')
    return render(request, 'tekstore/profile_edit_field.html')

# صفحه درخواست همکاری
def cooperation_request_view(request):
    return render(request, 'tekstore/cooperation_request.html')

# ثبت نظر برای محصول
@login_required
def add_product_comment(request, product_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        product = get_object_or_404(Product, pk=product_id)
        comment = ProductComment.objects.create(
            product=product,
            user=request.user,
            text=comment_text
        )
        messages.success(request, 'نظر شما با موفقیت ثبت شد.')
        return redirect('product_detail', pk=product_id)
    return redirect('product_detail', pk=product_id)

# ویو پنل کاربری برای بررسی وضعیت فروشندگی
@login_required
def user_dashboard(request):
    coop_requests = CooperationRequest.objects.filter(user=request.user)
    return render(request, 'tekstore/user_dashboard.html', {
        'coop_requests': coop_requests
    })

# ویو صفحه چت آنلاین (پشتیبانی)
@login_required
def chat_online(request):
    return render(request, 'tekstore/chat_online.html')

# چک می‌کنیم کاربر ادمین است و نام کاربری در لیست مجاز است
def admin_check(user):
    allowed_admins = ['admin1', 'admin2']
    return user.is_staff and user.username in allowed_admins

@login_required
@user_passes_test(admin_check)
def admin_chat_view(request):
    chats = Chat.objects.all().order_by('-created')
    return render(request, 'tekstore/admin_chat_list.html', {'chats': chats})

@login_required
@user_passes_test(admin_check)
def admin_chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.order_by('timestamp')
    return render(request, 'tekstore/admin_chat_detail.html', {
        'chat': chat,
        'messages': messages
    })

@login_required
@user_passes_test(admin_check)
def admin_chat_delete(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        chat.delete()
        messages.success(request, 'چت با موفقیت حذف شد.')
        return redirect('admin_chat_view')
    return render(request, 'tekstore/admin_chat_confirm_delete.html', {'chat': chat})
