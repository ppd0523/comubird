from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import *


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('nickname', 'email', 'created_date')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'password', )}),
        ("Personal info", {"fields": ('created_date',)}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'agreement', 'password1', 'password2')
        }),
    )
    readonly_fields = ('created_date', )
    search_fields = ('email', 'nickname')
    ordering = ('created_date', )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
