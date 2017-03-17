#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import sys
import time
import uuid
import django
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRO_ABSPATH = os.path.abspath(os.path.join(BASE_DIR, '../'))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, PRO_ABSPATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iEnglish.settings")
django.setup()

from testing.models import Level, Category, Word, Question, Paper

for item in Paper.objects.all():
    print '-------------------------'
    print item.username
    print '-------------------------'
    for que in item.questions.all():
        print que.name, que.categories
