# Generated by Django 3.1.4 on 2021-01-03 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20210103_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='child',
        ),
        migrations.AddField(
            model_name='node',
            name='child',
            field=models.ManyToManyField(to='courses.Node'),
        ),
    ]
