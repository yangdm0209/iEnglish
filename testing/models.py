#!/usr/bin/env python
# coding: utf-8
import random

from django.contrib.auth.models import User
from django.db.models import Q
from django.db import models
from django.utils import timezone

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
        return self.image.name if HTTP_FLAG in self.image.name else (
                                                                        CDN_FILES_URL + self.image.name) + '?imageView2/1/w/280/h/180'

    @property
    def get_thumb(self):
        return self.image.name if HTTP_FLAG in self.image.name else (
                                                                        CDN_FILES_URL + self.image.name) + '?imageView2/2/w/48'

    @property
    def total_word(self):
        return self.word.all().count()

    @property
    def total_test(self):
        return Paper.objects.filter(level=self.pk).count()

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
    level = models.ManyToManyField(Level, verbose_name='level', related_name='word')
    category = models.ManyToManyField(Category, verbose_name='category', related_name='word')

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Word, self).save(*args, **kwargs)
        info = get_word_info(self.word)
        self.pronunciation = info['pronunciation']
        self.audio = info['audio']
        self.definition = info['definition']

        return super(Word, self).save(*args, **kwargs)

    @property
    def make_ques(self):
        images = [w.get_image for w in random.sample(Word.objects.filter(~Q(id=self.pk)), 4)]
        index = random.randint(0, 3)
        images[index] = self.get_image
        return {'result': index, 'images': images}

    @property
    def get_image(self):
        return self.image.name if HTTP_FLAG in self.image.name else (
                                                                        CDN_FILES_URL + self.image.name) + '?imageView2/1/w/280/h/280'

    @property
    def get_thumb(self):
        return self.image.name if HTTP_FLAG in self.image.name else (
                                                                        CDN_FILES_URL + self.image.name) + '?imageView2/2/w/48'

    def __unicode__(self):
        return self.word

    class Meta:
        verbose_name_plural = 'Word'
        verbose_name = 'Word'


class Question(models.Model):
    RESULT_TP = ((0, 'wrong'), (1, 'right'))
    word = models.ForeignKey(Word, verbose_name='Word')
    result = models.IntegerField(choices=RESULT_TP, verbose_name='result')
    created_at = models.DateTimeField(verbose_name='CreateTime', default=timezone.now())

    def __unicode__(self):
        return self.word.word

    @property
    def get_result(self):
        for item in self.RESULT_TP:
            if item[0] == self.result:
                return item[1]

    @property
    def image(self):
        return self.word.get_image

    @property
    def audio(self):
        return self.word.audio

    @property
    def name(self):
        return self.word.word

    @property
    def categories(self):
        return [c.name for c in self.word.category.all()]


class Paper(models.Model):
    questions = models.ManyToManyField(Question, verbose_name='Questions', related_name='paper')
    user = models.ForeignKey(User, verbose_name='User')
    level = models.ForeignKey(Level, verbose_name='Level')
    score = models.IntegerField(verbose_name='Score', default=0)
    time = models.IntegerField(verbose_name='Finished in', default=0)
    created_at = models.DateTimeField(verbose_name='CreateTime', default=timezone.now())

    @property
    def date(self):
        return self.created_at.date()

    @property
    def username(self):
        return self.user.username

    @property
    def levelname(self):
        return self.level.name