# Generated by Django 4.2.7 on 2023-11-12 10:55

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
        ('user', '0002_usermodel_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='cards',
            field=models.ManyToManyField(default=builtins.any, to='card.card'),
        ),
    ]
