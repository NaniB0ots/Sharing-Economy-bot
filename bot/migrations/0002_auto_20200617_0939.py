# Generated by Django 3.0.4 on 2020-06-17 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tgusers',
            options={'ordering': ('-created',), 'verbose_name': 'пользователя', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
