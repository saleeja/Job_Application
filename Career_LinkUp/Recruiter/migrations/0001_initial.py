# Generated by Django 5.0.3 on 2024-03-22 08:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('required_qualifications', models.TextField()),
                ('desired_qualifications', models.TextField()),
                ('responsibilities', models.TextField()),
                ('application_deadline', models.DateTimeField(default=django.utils.timezone.now)),
                ('salary_range', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('job_type', models.CharField(choices=[('full-time', 'Full-time'), ('part-time', 'Part-time'), ('contract', 'Contract'), ('remote', 'Remote')], max_length=20)),
                ('company_benefits', models.TextField()),
                ('how_to_apply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
