# Generated by Django 3.0.4 on 2020-06-17 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vk_parser', '0006_delete_productсategory'),
        ('bot', '0002_auto_20200617_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgusers',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vk_parser.Cities', verbose_name='Город'),
        ),
    ]
