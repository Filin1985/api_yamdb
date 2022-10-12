# Generated by Django 2.2.16 on 2022-10-12 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Пользователь'), (2, 'Модератор'), (3, 'Админ')], null=True),
        ),
    ]
