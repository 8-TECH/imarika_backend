# Generated by Django 5.2.2 on 2025-06-12 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imarikapp', '0004_donate_partner_volunteer_delete_submission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donate',
            name='message',
        ),
    ]
