import secrets
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.timezone import now
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from djrichtextfield.models import RichTextField


# Overriding the default django authentication
"""
    this is for the basic sign-up for Appointment setters and Closers :)
"""
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, tel, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('You must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            tel= tel,
            nationality= nationality,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, tel, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            tel= tel,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, tel, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name= last_name,
            tel= tel,
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
    active = models.BooleanField(default=True)
    TC = models.BooleanField(default=False)#Terms and Conditions
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'tel', 'nationality']  # Email & Password are required by default.

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
    def has_agreed(self):
        """Is it a user?"""
        return self.TC

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


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(default='', blank=True, max_length=9)
    qrcode = models.ImageField(upload_to='user_QRC_auth/', blank=True)
    category = models.CharField(default='', max_length=25, choices=(('Closer', 'Closer'), ('Appointment_setter', 'Appointment_setter')), blank=True, null=True)
    nationality= CountryField(blank_label='(select country)')
    experience = models.CharField(default='', blank=True, max_length=9)
    resume = models.FileField(upload_to='resumes /% Y % m % d/', default='')
    skills = models.ManyToManyField('Skills')
    work_type = models.CharField(default='', max_length=25, choices=(('Full-time', 'Full-time'), ('Part-time', 'Part-time')), blank=True, null=True)
    cover_letter = RichTextField()
    created = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        concatenate = '%s%s%s' % (self.user, '-', self.code)
        return str(concatenate)

    def save(self, *args, **kwargs):
        qrcode_image = qrcode.make(f"Name: {self.user}\nAuthor: {self.code}")
        canvas = Image.new('RGB', (430, 430), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname = f"{'%s%s%s' % (self.user, '-', self.code)}.png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

class Skills(models.Model):
    skill = models.CharField(default='', blank=True, max_length=123)
    
    def __str__(self):
        return self.skill
    