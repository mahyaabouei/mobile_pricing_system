from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'is_active', 'admin', 'is_superuser')
    search_fields = ('username', 'phone', 'uniqidentifier', 'email')
    list_filter = ('admin', 'is_active', 'is_superuser', 'work_guarantee')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'company')}),
        ('اطلاعات مالی', {'fields': ('sheba_number', 'card_number', 'account_number', 'account_bank')}),
        ('سطح دسترسی', {'fields': ('admin', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('وضعیت', {'fields': ('work_guarantee', 'last_login', 'created_at', 'updated_at')}),
    )
