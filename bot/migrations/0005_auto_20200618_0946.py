# Generated by Django 3.0.7 on 2020-06-18 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vk_parser', '0007_productсategory'),
        ('bot', '0004_auto_20200617_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgusers',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vk_parser.Cities', verbose_name='Город'),
        ),
    ]
