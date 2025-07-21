from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Profile, CooperationRequest  # اضافه کردن مدل CooperationRequest

# فرم ثبت‌نام
class PersianSignUpForm(UserCreationForm):
    username = forms.CharField(label='نام کاربری', max_length=150)
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


# فرم ارسال تیکت
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'message']
        labels = {
            'subject': 'عنوان تیکت',
            'message': 'متن تیکت'
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'متن تیکت خود را وارد کنید...',
                'rows': 5,
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'عنوان تیکت خود را وارد کنید',
                'class': 'form-control'
            })
        }


# فرم اطلاعات کاربر (برای ویرایش پروفایل - نام، نام خانوادگی، ایمیل)
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='نام', required=False, widget=forms.TextInput(attrs={'class': 'form-control bg-light'}))
    last_name = forms.CharField(label='نام خانوادگی', required=False, widget=forms.TextInput(attrs={'class': 'form-control bg-light'}))
    email = forms.EmailField(label='ایمیل', required=False, widget=forms.EmailInput(attrs={'class': 'form-control bg-light'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# فرم اطلاعات پروفایل (تلفن، آدرس، عکس)
class ProfileForm(forms.ModelForm):
    phone = forms.CharField(label='شماره تماس', required=False, widget=forms.TextInput(attrs={
        'placeholder': 'مثلاً 09123456789',
        'class': 'form-control bg-light'
    }))
    address = forms.CharField(label='آدرس', required=False, widget=forms.Textarea(attrs={
        'rows': 2,
        'class': 'form-control bg-light',
        'placeholder': 'آدرس دقیق پستی...'
    }))
    image = forms.ImageField(label='عکس پروفایل', required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control bg-light'
    }))

    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']


# فرم درخواست همکاری
class CooperationRequestForm(forms.ModelForm):
    phone = forms.CharField(label='شماره تماس', widget=forms.TextInput(attrs={
        'placeholder': 'مثلاً 09123456789',
        'class': 'form-control'
    }))
    products = forms.CharField(label='محصولات ارائه شده', widget=forms.TextInput(attrs={
        'placeholder': 'مثلاً تولید سخت‌افزار، تعمیرات ...',
        'class': 'form-control'
    }))
    details = forms.CharField(label='توضیحات تکمیلی', widget=forms.Textarea(attrs={
        'placeholder': 'توضیحات بیشتر درباره همکاری...',
        'rows': 4,
        'class': 'form-control'
    }))

    class Meta:
        model = CooperationRequest
        fields = ['phone', 'products', 'details']
