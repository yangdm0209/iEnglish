#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from testing.models import Level, Category, Word, Paper


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'words', 'show_image']
    list_display_links = ['name']
    fields = ['name', 'words', 'image']

    def show_image(self, obj):
        url = obj.get_thumb
        return mark_safe('<img width="48" height="48"  src = "%s" />' % url)

    show_image.short_description = 'image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_image']
    list_display_links = ['name']
    fields = ['name', 'image']

    def show_image(self, obj):
        url = obj.get_thumb
        return mark_safe('<img width="48" height="48"  src = "%s" />' % url)

    show_image.short_description = 'image'


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'show_image', 'show_audio', 'pronunciation', 'definition', 'levels', 'categories']
    list_display_links = ['word']
    fields = ['word', 'image', 'level', 'category']

    def show_image(self, obj):
        url = obj.get_thumb
        return mark_safe('<img width="48" height="48"  src = "%s" />' % url)

    def show_audio(self, obj):
        if obj.audio:
            return mark_safe(
                '<audio src="%s" controls="controls">Your browser does not support the audio tag.</audio>' % obj.audio)
        else:
            return 'Cannot get audio for this word, plz check the word!'

    def levels(self, obj):
        ret = 'Levels:<ul>'
        for item in obj.level.all():
            ret += '<li>%s</li>' % item.name
        ret += '</ul>'
        return mark_safe(ret)

    def categories(self, obj):
        ret = 'Categories:<ul>'
        for item in obj.category.all():
            ret += '<li>%s</li>' % item.name
        ret += '</ul>'
        return mark_safe(ret)

    show_image.short_description = 'image'
    show_audio.short_description = 'audio'


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'score', 'time', 'created_at', 'show_question']
    readonly_fields = ['user', 'level', 'score', 'time', 'created_at', 'questions']

    def show_question(self, obj):
        ret = 'Words:<ul>'
        for item in obj.questions.all():
            ret += '<li>%s  ---- %s</li>' % (item.word, item.get_result)
        ret += '</ul>'
        return mark_safe(ret)

    show_question.short_description = 'questions'
