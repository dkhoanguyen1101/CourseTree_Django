# Generated by Django 3.1.4 on 2020-12-28 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20201228_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='num',
            field=models.IntegerField(choices=[(201, 201)]),
        ),
    ]
