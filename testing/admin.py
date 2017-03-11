#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from testing.models import Level, Category, Word


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
    list_display = ['word', 'show_image', 'show_audio', 'pronunciation', 'definition']
    list_display_links = ['word']
    fields = ['word', 'image']

    def show_image(self, obj):
        url = obj.get_thumb
        return mark_safe('<img width="48" height="48"  src = "%s" />' % url)

    def show_audio(self, obj):
        if obj.audio:
            return mark_safe(
                '<audio src="%s" controls="controls">Your browser does not support the audio tag.</audio>' % obj.audio)
        else:
            return 'Cannot get audio for this word, plz check the word!'

    show_image.short_description = 'image'
    show_audio.short_description = 'audio'
