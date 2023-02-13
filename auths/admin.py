from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, UserProfile, Skills, Language, Days, ClientProfile, ExtraField, Sales_Offer, Trainers

admin.site.site_header = 'UpgradeProfits~~test Admin'
admin.site.index_title = 'Admin'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin', 'first_name', 'last_name', 'tel', 'category')
    list_filter = ('admin', 'TC')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'tel', 'category')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'TC')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'tel', 'category')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'tel', 'category')
    ordering = ('email', 'first_name', 'last_name', 'tel', 'category')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Skills)
admin.site.register(Language)
admin.site.register(Days)
admin.site.register(ExtraField)
admin.site.register(Sales_Offer)
admin.site.register(Trainers)
# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)


admin.site.register(ClientProfile)
