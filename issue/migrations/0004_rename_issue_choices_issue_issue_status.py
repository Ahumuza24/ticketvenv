# Generated by Django 5.0.6 on 2024-06-25 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0003_issue_issue_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='issue_choices',
            new_name='issue_status',
        ),
    ]
