#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
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

# with open('template.csv', 'rb') as f:
#     spamreader = csv.reader(f, delimiter=',', quotechar='|')
#     for row in spamreader:
#         for item in row:
#             print item.decode('gbk'),
#         print

with open('eggs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely,Spam', 'Wonderful,Spam'])
