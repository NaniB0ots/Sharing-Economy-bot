# -*- coding: utf-8 -*-

from django.db import models
from vk_parser.models import Cities, ProductСategory

from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User


class TGUsers(models.Model):
    chat_id = models.IntegerField('chat_id', unique=True)
    city = models.ForeignKey(Cities, verbose_name=u'Город', on_delete=models.DO_NOTHING, null=True)
    categories = models.ManyToManyField(ProductСategory, verbose_name=u'Категория')

    created = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.chat_id)
