# Generated by Django 5.0.3 on 2024-03-22 18:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobSeeker', '0002_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='applicant_email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='cover_letter',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer/Recruiter')], max_length=20),
        ),
    ]
