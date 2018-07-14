from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from .models import AuthUser


class AuthUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions',
                                       'roles', 'tags')}))
    list_display = ('full_name', 'username')
    list_filter = ('roles',)


admin.site.register(AuthUser, AuthUserAdmin)
