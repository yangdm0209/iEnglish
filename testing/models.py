#!/usr/bin/env python
# coding: utf-8

from django.db import models
from util.constants import CDN_FILES_URL, HTTP_FLAG
from util.tools_method import AdminStorageToQiniu, get_word_info


# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=64, verbose_name='name')
    words = models.IntegerField(verbose_name='max words per paper', default=20)
    image = models.FileField(upload_to="images/%Y/%m/%d", max_length=255, storage=AdminStorageToQiniu(),
                             verbose_name='image', default="default.jpg")

    @property
    def get_image(self):
        return self.image.name if HTTP_FLAG in self.image.name else (CDN_FILES_URL + self.image.name)

    @property
    def get_thumb(self):
        return self.image.name if HTTP_FLAG in self.image.name else (
                                                                        CDN_FILES_URL + self.image.name) + '?imageView2/2/w/48'

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Level'
        verbose_name = 'Level'


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='name')
    image = models.FileField(upload_to="images/%Y/%m/%d", max_length=255, storage=AdminStorageToQiniu(),
                             verbose_name='image', default="default.jpg")

    @property
    def get_image(self):
        return self.image.name if HTTP_FLAG in self.image.name else (CDN_FILES_URL + self.image.name)

    @property
    def get_thumb(self):
        return self.image.name if HTTP_FLAG in self.image.name else (
                                                                        CDN_FILES_URL + self.image.name) + '?imageView2/2/w/48'

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Category'
        verbose_name = 'Category'


class Word(models.Model):
    word = models.CharField(max_length=128, verbose_name='word')
    image = models.FileField(upload_to="images/%Y/%m/%d", max_length=255, storage=AdminStorageToQiniu(),
                             verbose_name='image', default="default.jpg")
    audio = models.CharField(max_length=255, verbose_name="audio", default='')
    pronunciation = models.CharField(max_length=255, verbose_name='pronunciation', default='')
    definition = models.CharField(max_length=255, verbose_name='definition', default='')

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Word, self).save(*args, **kwargs)
        info = get_word_info(self.word)
        self.pronunciation = info['pronunciation']
        self.audio = info['audio']
        self.definition = info['definition']

        return super(Word, self).save(*args, **kwargs)

    @property
    def get_image(self):
        return self.image.name if HTTP_FLAG in self.image.name else (CDN_FILES_URL + self.image.name)

    @property
    def get_thumb(self):
        return self.image.name if HTTP_FLAG in self.image.name else (
                                                                        CDN_FILES_URL + self.image.name) + '?imageView2/2/w/48'

    def __unicode__(self):
        return self.word

    class Meta:
        verbose_name_plural = 'Word'
        verbose_name = 'Word'
