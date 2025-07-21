from django import template

register = template.Library()

# فیلتر add_class
@register.filter
def add_class(value, arg):
    """
    این فیلتر برای اضافه کردن کلاس‌های CSS به فیلدهای فرم استفاده می‌شود.
    :param value: فیلد فرم
    :param arg: کلاس CSS که می‌خواهیم به فیلد اضافه کنیم
    """
    return value.as_widget(attrs={'class': arg})
