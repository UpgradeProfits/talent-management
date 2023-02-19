from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

# Create your models here.
class AddVacancy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    job_title = models.CharField(default='', max_length=250, blank=False)
    company_name = models.CharField(default='', max_length=250, blank=True)
    category = models.CharField(default='', max_length=125, choices=(('Closer', 'Closer'), ('Appointment setter', 'Appointment setter'), ('Closer & Appointment setter', 'Closer & Appointment setter')), blank=True, null=True)
    job_type = models.CharField(default='', max_length=25, choices=(('Full-time', 'Full-time'), ('Part-time', 'Part-time')), blank=True, null=True)
    pay_type = models.CharField(default='', blank=True, max_length=25, choices=(('Hourly', 'Hourly'), ('Commission', 'Commission'), ('Hourly With Commission', 'Hourly With Commission')))
    expected_commission=models.IntegerField(default=0, blank=True)
    expected_hourly_pay=models.IntegerField(default=0, blank=True)
    hourly_plus = models.IntegerField(default=0, blank=True)
    job_description = RichTextField(blank=False)
    status = models.CharField(default='open', max_length=25, choices=(('open', 'open'), ('closed', 'closed')), blank=True)

    def __str__(self):
        return str(self.job_title)

class Apply(models.Model):
    job = models.ForeignKey('AddVacancy', null=True, blank=True, on_delete=models.CASCADE)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    link = models.URLField(max_length = 200,  blank=True)
    hire = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(f'{self.job} applied by {self.by}')