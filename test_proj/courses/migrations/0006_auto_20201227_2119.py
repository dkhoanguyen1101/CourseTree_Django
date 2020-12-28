# Generated by Django 3.1.4 on 2020-12-28 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20201227_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='MainCourse',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course'),
        ),
        migrations.AlterField(
            model_name='node',
            name='num',
            field=models.IntegerField(choices=[('201', 201)]),
        ),
    ]
