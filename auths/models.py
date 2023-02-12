import secrets
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File
from django_countries.fields import CountryField
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField


# Overriding the default django authentication
"""
    this is for the basic sign-up for Appointment setters and Closers :)
"""
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('You must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            password=password
        )
        user.active=True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    first_name= models.CharField(default='', null=False, blank=False, max_length=30)
    last_name= models.CharField(default='', null=False, blank=False, max_length=30)
    tel = PhoneNumberField()
    added = models.DateTimeField(auto_now=True)
    category = models.CharField(default='', max_length=255, choices=(('client', 'client'), ('seeker', 'seeker')))
    authenticated = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    TC = models.BooleanField(default=False)#Terms and Conditions
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # created = models.DateTimeField(auto_now_add=True, auto_created=datetime.now())
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Email & Password are required by default.

    # def save():
    #     mssg = f'Account created for {firstname}'
    #     message = f""" Hi {firstname} {lastname} \n welcome to Talent-Mangement, 
    #     please do verify your account so we can tell you are wonderful person :) \n \n \n
    #     Tech Team
    #     """
    #     subject = f'verify account for {email}'
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [email, ]
    #     send_mail( subject, message, email_from, recipient_list, fail_silently=False)
    #     pass

    def get_full_name(self):
        # The user is identified by their first&last name
        fullname = '%s %s' % (self.first_name, self.last_name)
        return fullname

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):  # __unicode__ on Python 2
        fullname = '%s %s' % (self.first_name, self.last_name)
        return fullname

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin
    @property
    def is_active(self):
        """Is the user active?"""
        return self.active



class ClientProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    display_photo= models.ImageField(upload_to='clients/', blank=True)
    full_name = models.CharField(max_length=250, default='', blank=True)
    company_name = models.CharField(max_length=100, default='', blank=True)
    preffered_lang = models.CharField(max_length=100, default='', blank=True)
    about = RichTextField(blank=False)
    
    def __str__(self):
        return str(self.user)

class UserProfile(models.Model):
    OPTIONS = (
        ('Yes', 'Yes'),
        ('No', 'No'), 
    )
    
    Availabity = (
        ('I am Ready To Start Now!', 'I am Ready To Start Now!'),
        ('I will be working In 1 Month', 'I will be working In 1 Month'),
        ('I will be working In 2 Month', 'I will be working In 2 Month')
    )
    

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(default='', blank=True, max_length=255)
    last_name = models.CharField(default='', blank=True, max_length=255)
    slug = models.SlugField(blank=True)
    display_photo= models.ImageField(upload_to='closers/', blank=True)
    code = models.CharField(default='', blank=True, max_length=9)
    qrcode = models.ImageField(upload_to='user_QRC_auth/', blank=True)
    gender = models.CharField(default="Male", max_length=6, blank=True, choices=(('Male', 'Male'), ('Female', 'Female')))
    category = models.CharField(default='', max_length=125, choices=(('Closer', 'Closer'), ('Appointment_setter', 'Appointment_setter'), ('Closer & Appointment_setter', 'Closer & Appointment_setter')), blank=True, null=True)
    nationality= CountryField(blank_label='(select country)')
    city = models.CharField(default='', max_length=100, blank=True)
    zip_code = models.CharField(default='', max_length=20, blank=True)
    location = CountryField(blank_label='(select location)')
    experience = models.CharField(default='', blank=True, max_length=9)
    resume = models.FileField(upload_to=f'resumes/', default='')
    document_type = models.FileField(upload_to=f'extras/', default='')
    education = models.CharField(default='', blank=True, max_length=255)
    skills = models.ForeignKey('Skills', blank=True, on_delete=models.CASCADE, null=True)
    work_type = models.CharField(default='', max_length=25, choices=(('Full-time', 'Full-time'), ('Part-time', 'Part-time')), blank=True, null=True)
    preferred_niche_to_sell = models.CharField(default='', max_length=100, choices=(('Business Coaching', 'Business Coaching'), ('Marketing & Advertising', 'Marketing & Advertising'), ('Personal Development', 'Personal Development'),('Spirituality Coaching', 'Spirituality Coaching'),('Insurance', 'Insurance'),('Innovative Software', 'Innovative Software'),
    ('Relationship Coaching', 'Relationship Coaching'),('Real Estate(Real Estate Agents/Mortgage)', 'Real Estate(Real Estate Agents/Mortgage)'),('Real Estate Investing', 'Real Estate Investing'),('Finance/Investing', 'Finance/Investing'),('Finance/Investing', 'Finance/Investing'),
    ('Fitness', 'Fitness'),('Religious Coaching', 'Religious Coaching'),('Software Sales', 'Software Sales'),('Enterprise Sales', 'Enterprise Sales'),('Home Improvement & Security', 'Home Improvement & Security'),('Recruiting Services', 'Recruiting Services')))
    days_available = models.ForeignKey('Days', blank=True, on_delete=models.CASCADE, null=True)
    hours_available = models.IntegerField(default=0, blank=True)
    call_per_day = models.IntegerField(default=0, blank=True)
    outbound_calls_per_day = models.IntegerField(default=0, blank=True)
    appointments_per_day = models.IntegerField(default=0, blank=True)
    income_per_month = models.IntegerField(default=0, blank=True)
    ticket_size = models.IntegerField(default=0, blank=True)
    highest_tickets = models.IntegerField(default=0, blank=True)
    highest_ticket_product = models.CharField(default='', blank=True, max_length=100)
    total_revenue_sales_career = models.IntegerField(default=0, blank=True)
    total_revenue_sales_three_yrs = models.IntegerField(default=0, blank=True)
    generated_revenue = models.IntegerField(default=0, blank=True)
    pay = models.CharField(default='', blank=True, max_length=10, choices=(('Hourly', 'Hourly'), ('Commission', 'Commission'), ('Hourly+', 'Hourly+')))
    expected_commission=models.IntegerField(default=0, blank=True)
    expected_hourly_pay=models.IntegerField(default=0, blank=True)
    Why_are_you_interested_in_remote_sales = models.TextField(default='', blank=True, max_length=500)
    deal_breaker_for_you = models.TextField(default='', blank=True, max_length=500)
    What_offers_worked_on = models.TextField(default='', blank=True, max_length=500)
    what_niche = models.CharField(default="", max_length=100, blank=True)
    language = models.ForeignKey('Language', blank=True, on_delete=models.CASCADE, null=True)
    are_you_comfortable_with_commission_based_pay = models.CharField(max_length=255, choices=OPTIONS)
    past_trainings = models.CharField(default="", max_length=300, blank=True)
    past_leade_gen = models.CharField(max_length=255, choices=OPTIONS)
    reason = models.TextField(default='', blank=True, max_length=500)
    offers_worked_on_niche_and_ticket_price = models.CharField(default="", max_length=300, blank=True)
    offers_worked_on_past_years = models.CharField(default="", max_length=300, blank=True)
    reason_for_leaving_last_position = models.TextField(default='', blank=True, max_length=500)
    how_does_a_sales_fit_your_goals= models.TextField(default='', blank=True, max_length=500)
    average_units_sold = models.IntegerField(default=0, blank=True)
    average_tickets_sold = models.IntegerField(default=0, blank=True)
    timezone = models.CharField(default='', blank=True, max_length=100)
    profile_video = models.FileField(upload_to=f'profile_videos/', default='', blank=True)
    cover_letter = models.TextField(default='', blank=True, max_length=500)
    achievements = models.TextField(default='', blank=True, max_length=500)
    anything_else_important_to_you_that_we_should_know = models.TextField(default='', blank=True, max_length=500)
    verified = models.BooleanField(default=False, blank=True)
    start_date = models.CharField(default='', max_length=123, blank=True, choices=Availabity)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        if self.verified == True:
            concatenate = '%s%s' % (self.user, ' (verified)')
        else:
            concatenate = '%s%s' % (self.user, ' (unverified)')
        return str(concatenate)

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.first_name}-{self.last_name}')
        qrcode_image = qrcode.make(f"Name: {self.user}\nUser: {self.code}")
        canvas = Image.new('RGB', (430, 430), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname = f"{'%s%s%s' % (self.user, '-', self.code)}.png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        super(UserProfile, self).save(*args, **kwargs)

class Skills(models.Model):
    skill = models.CharField(default='', blank=True, max_length=123)
    
    def __str__(self):
        return self.skill


class Language(models.Model):
    name = models.CharField(default="", max_length=90, blank=True)
    
    def __str__(self):
        return str(self.name)

class Days(models.Model):

    day= models.CharField(default="", max_length=1, blank=False)
    def __str__(self):
        return str(self.day)

class Country(models.Model):
    country= CountryField(blank_label='(select country)')
    
    def __str__(self):
        return str(self.country)

class ExtraField(models.Model):
    SALES_OPTION = (
        ('1 sales', '1 sales'),
        ('2 sales', '2 sales')
    )

    LEADS_OPTION = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    sales_process = models.CharField(default='select', max_length=30, choices=SALES_OPTION)
    lead_generation = models.CharField(default='select', max_length=3, choices=LEADS_OPTION)
    past_sales_training = models.ForeignKey('Trainers', on_delete=models.CASCADE)
    created = models.DateTimeField(default=now)

    
    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user}-{self.past_sales_training}')
        super(ExtraField, self).save(*args, **kwargs)

class Trainers(models.Model):
    name =  models.CharField(default='', max_length=200)
    
    def __str__(self):
        return str(self.name)

class Sales_Offer(models.Model):
    with_field = models.ForeignKey('Trainers', on_delete=models.CASCADE)
    date = models.DateField()
    niche = models.CharField(default='', max_length=100)
    total_generated_rev = models.CharField(default='', max_length=100)
    avg_ticket = models.CharField(default='', max_length=100)

    def __str__(self):
        return str(self.with_field)