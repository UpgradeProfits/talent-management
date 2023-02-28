# Generated by Django 4.0 on 2023-02-25 01:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('added', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[('client', 'client'), ('seeker', 'seeker')], default='', max_length=255)),
                ('authenticated', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('TC', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True)),
                ('sales_process', models.CharField(choices=[('1 call close', '1 call close'), ('2 call close', '2 call close'), ('Enterprise deals', 'Enterprise deals')], default='select', max_length=30)),
                ('lead_generation', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='select', max_length=3)),
                ('last_avg_sales', models.CharField(blank=True, default='', max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(blank=True, default='', max_length=123)),
            ],
        ),
        migrations.CreateModel(
            name='Timezone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(blank=True, default='', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Trainers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='', max_length=255)),
                ('last_name', models.CharField(blank=True, default='', max_length=255)),
                ('slug', models.SlugField(blank=True)),
                ('display_photo', models.ImageField(blank=True, upload_to='closers/')),
                ('code', models.CharField(blank=True, default='', max_length=9)),
                ('qrcode', models.ImageField(blank=True, upload_to='user_QRC_auth/')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=6)),
                ('category', models.CharField(blank=True, choices=[('Closer', 'Closer'), ('Appointment setter', 'Appointment setter'), ('Closer & Appointment setter', 'Closer & Appointment setter')], default='', max_length=125, null=True)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('address', models.CharField(blank=True, default='', max_length=250)),
                ('city', models.CharField(blank=True, default='', max_length=100)),
                ('zip_code', models.CharField(blank=True, default='', max_length=20)),
                ('state', models.CharField(blank=True, default='', max_length=100)),
                ('experience', models.CharField(blank=True, default='', max_length=9)),
                ('resume', models.FileField(blank=True, default='', upload_to='resumes/')),
                ('education', models.CharField(blank=True, default='', max_length=255)),
                ('work_type', models.CharField(blank=True, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')], default='', max_length=25, null=True)),
                ('preferred_niche_to_sell', models.CharField(choices=[('Business Coaching', 'Business Coaching'), ('Enterprise Sales', 'Enterprise Sales'), ('Finance/Investing', 'Finance/Investing'), ('Fitness', 'Fitness'), ('Home Improvement & Security', 'Home Improvement & Security'), ('Innovative Software', 'Innovative Software'), ('Insurance', 'Insurance'), ('Marketing & Advertising', 'Marketing & Advertising'), ('Personal Development', 'Personal Development'), ('Real Estate (Real Estate Agents/Mortgage)', 'Real Estate (Real Estate Agents/Mortgage)'), ('Real Estate Investing', 'Real Estate Investing'), ('Recruiting Services', 'Recruiting Services'), ('Relationship Coaching', 'Relationship Coaching'), ('Religious Coaching', 'Religious Coaching'), ('Software Sales', 'Software Sales'), ('Solar', 'Solar'), ('Spirituality Coaching', 'Spirituality Coaching'), ('Other', 'Other')], default='', max_length=100)),
                ('hours_available', models.IntegerField(blank=True, default=0)),
                ('call_per_day', models.IntegerField(blank=True, default=0)),
                ('outbound_calls_per_day', models.IntegerField(blank=True, default=0)),
                ('appointments_per_day', models.IntegerField(blank=True, default=0)),
                ('income_per_month', models.IntegerField(blank=True, default=0)),
                ('ticket_size', models.IntegerField(blank=True, default=0)),
                ('highest_tickets', models.IntegerField(blank=True, default=0)),
                ('highest_ticket_product', models.CharField(blank=True, default='', max_length=100)),
                ('total_revenue_sales_career', models.IntegerField(blank=True, default=0)),
                ('total_revenue_sales_three_yrs', models.IntegerField(blank=True, default=0)),
                ('generated_revenue', models.IntegerField(blank=True, default=0)),
                ('pay', models.CharField(blank=True, choices=[('Hourly', 'Hourly'), ('Commission', 'Commission'), ('Hourly_with_commission', 'Hourly with commission')], default='', max_length=30)),
                ('expected_commission', models.IntegerField(blank=True, default=0)),
                ('expected_hourly_pay', models.IntegerField(blank=True, default=0)),
                ('commission', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('hourly_commission', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('Why_are_you_interested_in_remote_sales', models.TextField(blank=True, default='', max_length=500)),
                ('deal_breaker_for_you', models.TextField(blank=True, default='', max_length=500)),
                ('What_offers_worked_on', models.TextField(blank=True, default='', max_length=500)),
                ('what_niche', models.CharField(blank=True, default='', max_length=100)),
                ('are_you_comfortable_with_commission_based_pay', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=255, null=True)),
                ('past_trainings', models.CharField(blank=True, default='', max_length=300)),
                ('past_leade_gen', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=255)),
                ('reason', models.TextField(blank=True, default='', max_length=500)),
                ('offers_worked_on_niche_and_ticket_price', models.CharField(blank=True, default='', max_length=300)),
                ('offers_worked_on_past_years', models.CharField(blank=True, default='', max_length=300)),
                ('reason_for_leaving_last_position', models.TextField(blank=True, default='', max_length=500)),
                ('how_does_a_sales_fit_your_goals', models.TextField(blank=True, default='', max_length=500)),
                ('average_units_sold', models.IntegerField(blank=True, default=0)),
                ('average_tickets_sold', models.IntegerField(blank=True, default=0)),
                ('profile_video', models.FileField(blank=True, default='', upload_to='profile_videos/')),
                ('cover_letter', models.TextField(blank=True, default='', max_length=500)),
                ('achievements', models.TextField(blank=True, default='', max_length=500)),
                ('anything_else_important_to_you_that_we_should_know', models.TextField(blank=True, default='', max_length=500)),
                ('verified', models.BooleanField(blank=True, default=False)),
                ('start_date', models.CharField(blank=True, choices=[('I am Ready To Start Now!', 'I am Ready To Start Now!'), ('I will be working In 1 Month', 'I will be working In 1 Month'), ('I will be working In 2 Month', 'I will be working In 2 Month')], default='', max_length=123)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('days_available', models.ManyToManyField(blank=True, to='auths.Days')),
                ('language', models.ManyToManyField(blank=True, null=True, to='auths.Language')),
                ('skills', models.ManyToManyField(blank=True, null=True, to='auths.Skills')),
                ('timezones', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auths.timezone')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auths.user')),
            ],
        ),
        migrations.CreateModel(
            name='Sales_Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('niche', models.CharField(default='', max_length=100)),
                ('total_generated_rev', models.CharField(default='', max_length=100)),
                ('avg_ticket', models.CharField(default='', max_length=100)),
                ('with_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auths.extrafield')),
            ],
        ),
        migrations.AddField(
            model_name='extrafield',
            name='past_sales_training',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auths.trainers'),
        ),
        migrations.AddField(
            model_name='extrafield',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auths.user'),
        ),
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_photo', models.ImageField(blank=True, upload_to='clients/')),
                ('profile_video', models.FileField(blank=True, default='', upload_to='clients/profile_videos/')),
                ('full_name', models.CharField(blank=True, default='', max_length=250)),
                ('workers', models.CharField(blank=True, choices=[('Closers', 'Closers'), ('Appointment Setters', 'Appointment Setters'), ('Appointment Setters & Closers', 'Appointment Setters & Closers')], default='', max_length=100)),
                ('niche', models.CharField(choices=[('Business Coaching', 'Business Coaching'), ('Marketing & Advertising', 'Marketing & Advertising'), ('Personal Development', 'Personal Development'), ('Spirituality Coaching', 'Spirituality Coaching'), ('Insurance', 'Insurance'), ('Innovative Software', 'Innovative Software'), ('Relationship Coaching', 'Relationship Coaching'), ('Real Estate(Real Estate Agents/Mortgage)', 'Real Estate(Real Estate Agents/Mortgage)'), ('Real Estate Investing', 'Real Estate Investing'), ('Finance/Investing', 'Finance/Investing'), ('Finance/Investing', 'Finance/Investing'), ('Fitness', 'Fitness'), ('Religious Coaching', 'Religious Coaching'), ('Software Sales', 'Software Sales'), ('Enterprise Sales', 'Enterprise Sales'), ('Home Improvement & Security', 'Home Improvement & Security'), ('Recruiting Services', 'Recruiting Services')], default='----', max_length=100)),
                ('what_do_you_sell', models.TextField(blank=True, default='', max_length=100)),
                ('price_range', models.IntegerField(blank=True, default=0)),
                ('earnings_you_offer', models.CharField(blank=True, default='', max_length=100)),
                ('days', models.CharField(choices=[('Monday-Friday', 'Monday-Friday'), ('Monday-Saturday', 'Monday-Saturday'), ('Monday-Sunday', 'Monday-Sunday'), ('Weekends Only', 'Weekends Only')], default='', max_length=20)),
                ('appointments_booked', models.IntegerField(blank=True, default=0)),
                ('preffered_lang', models.CharField(blank=True, default='', max_length=100)),
                ('timezones', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auths.timezone')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auths.user')),
            ],
        ),
    ]
