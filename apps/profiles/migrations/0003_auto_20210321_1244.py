# Generated by Django 3.1.7 on 2021-03-21 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210321_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrequest',
            name='status',
            field=models.CharField(choices=[('send', 'send'), ('accepted', 'accepted'), ('rejected', 'rejected')], max_length=8),
        ),
    ]
