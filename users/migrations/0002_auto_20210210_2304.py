# Generated by Django 3.1.6 on 2021-02-10 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
