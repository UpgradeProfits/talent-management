from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Closer, Skills

admin.site.site_header = 'UpgradeProfits~~test Admin'
admin.site.index_title = 'Admin'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin', 'first_name', 'last_name', 'tel',)
    list_filter = ('admin', 'TC')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'tel', )}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'TC')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'tel')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'tel')
    ordering = ('email', 'first_name', 'last_name', 'tel')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Closer)
admin.site.register(Skills)
# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)


# admin.site.register(UserBio)
