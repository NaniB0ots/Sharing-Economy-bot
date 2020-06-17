# -*- coding: utf-8 -*-

from django.db import models
from vk_parser.models import Cities

from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User


class TGUsers(models.Model):
    chat_id = models.IntegerField('chat_id', unique=True)
    city = models.ForeignKey(Cities, verbose_name=u'Город', on_delete=models.DO_NOTHING)

    vegetables_fruits_nuts = models.BooleanField('Овощи фрукты, орехи')
    cereals_pasta = models.BooleanField('Крупы, макаронные изделия')
    meat_fish = models.BooleanField('Мясное, рыба')
    juices_water = models.BooleanField('Соки, воды')
    bakery_confectionery_products = models.BooleanField('Хлебобулочные и кондитерские изделия')
    canned_food = models.BooleanField('Консервы')
    alcohol = models.BooleanField('Алкоголь')
    dairy_products = models.BooleanField('Молочная продукция')
    ready_meals = models.BooleanField('Готовые блюда')

    created = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.chat_id)
