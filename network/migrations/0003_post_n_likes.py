# Generated by Django 3.0.3 on 2021-05-27 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20200722_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='n_likes',
            field=models.IntegerField(default=0),
        ),
    ]
