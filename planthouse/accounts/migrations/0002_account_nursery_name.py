# Generated by Django 3.0.4 on 2020-06-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='nursery_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]