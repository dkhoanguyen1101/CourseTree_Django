# Generated by Django 3.1.4 on 2020-12-28 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='note',
        ),
    ]
