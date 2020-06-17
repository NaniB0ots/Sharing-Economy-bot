# -*- coding: utf-8 -*-

from django.db import models
from vk_parser.models import Cities, ProductСategory

from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User

CATEGORIES = {1: 'Овощи фрукты, орехи', 2: 'Крупы, макаронные изделия', 3: 'Мясное, рыба', 4: 'Соки, воды',
              5: 'Хлебобулочные и кондитерские изделия', 6: 'Консервы', 7: 'Алкоголь', 8: 'Молочная продукция',
              9: 'Готовые блюда'}


class TGUsers(models.Model):
    chat_id = models.IntegerField('chat_id', unique=True)
    city = models.ForeignKey(Cities, verbose_name=u'Город', on_delete=models.DO_NOTHING)
    categories = models.ManyToManyField(ProductСategory, verbose_name=u'Категория')

    created = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.chat_id)
