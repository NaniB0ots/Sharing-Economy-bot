# -*- coding: utf-8 -*-
from django.db import models


class Cities(models.Model):
    name = models.CharField('Город', max_length=250, unique=True)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class VKGroups(models.Model):
    title = models.CharField('Название группы', max_length=250)
    city = models.ForeignKey(Cities, verbose_name=u'Город', on_delete=models.DO_NOTHING)
    group_id = models.CharField('id группы', max_length=250)

    created = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'группу'
        verbose_name_plural = 'Вк группы'

    def __str__(self):
        return self.title



