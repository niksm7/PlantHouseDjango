# Generated by Django 3.0.4 on 2020-06-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursery', '0005_auto_20200609_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nursery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
