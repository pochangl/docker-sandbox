# Generated by Django 2.2.6 on 2019-11-15 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_problem_output_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='image',
            field=models.CharField(default='python:3.7', max_length=128),
            preserve_default=False,
        ),
    ]
