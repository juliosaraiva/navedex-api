# Generated by Django 3.1 on 2020-08-13 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='navers',
        ),
    ]
