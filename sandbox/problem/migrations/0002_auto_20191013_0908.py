# Generated by Django 2.2.6 on 2019-10-13 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='error',
            new_name='stderr',
        ),
    ]
