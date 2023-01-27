from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django import forms
from .models import User, UserProfile, Country, ClientProfile, Language
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from djrichtextfield.widgets import RichTextWidget


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2



    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
class UserProfileForm(forms.ModelForm):
    # cover_letter = forms.CharField(widget=RichTextWidget())
    class Meta:
        model = UserProfile
        fields = "__all__"
            # 'profile_video',
            # 'first_name',
            # 'last_name',
            # 'city',
            # 'location',
            # 'nationality',
            # 'zip_code',
            # 'gender',
            # 'resume',
            # 'document_type',
            # 'start_date',
            # 'preferred_niche_to_sell',
            # 'category',
            # 'outbound_calls_per_day',
            # 'highest_ticket_product',
            # 'pay',
            # 'expected_hourly_pay',
            # 'expected_commission',
            # 'are_you_comfortable_with_commission_based_pay',
            # 'total_revenue_sales_career',
            # 'total_revenue_sales_three_yrs',
            # 'generated_revenue',
            # 'ticket_size',
            # 'highest_tickets',
            # 'past_trainings',
            # 'Why_are_you_interested_in_remote_sales',
            # 'deal_breaker_for_you',
            # 'average_tickets_sold',
            # 'average_units_sold',
            # 'offers_worked_on_past_years',
            # 'language',
            # 'skills',
            # 'days_available',
            # 'past_leade_gen',
            # 'reason',
            # 'offers_worked_on_niche_and_ticket_price',
            # 'reason_for_leaving_last_position',
            # 'how_does_a_sales_fit_your_goals',
            # 'education',
            # 'experience',
            # 'achievements',
            # 'cover_letter',
            # 'anything_else_important_to_you_that_we_should_know',

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = "__all__"

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = "__all__"

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = "__all__"