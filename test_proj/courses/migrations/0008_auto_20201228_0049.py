# Generated by Django 3.1.4 on 2020-12-28 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20201227_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='num',
            field=models.CharField(max_length=5),
        ),
    ]