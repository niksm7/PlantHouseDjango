# Generated by Django 3.0.4 on 2020-06-08 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='nursery/images'),
        ),
    ]