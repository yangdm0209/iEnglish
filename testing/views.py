# !/usr/bin/env python
# coding: utf-8
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
import random

# Create your views here.
from django.template import RequestContext
from django.template.defaultfilters import register
from django.utils.safestring import SafeString

from testing.models import Level


def main(request):
    return HttpResponseRedirect('/know/')
    # return render_to_response('main.html',
    #                           RequestContext(request))


@login_required
def know(request):
    levels = Level.objects.all()
    return render_to_response('know.html',
                              RequestContext(request, {'know_active': 1, 'levels': levels}))


@register.filter('list')
def do_list(value):
    return range(1, value + 1)


@login_required
def test(request, level_id):
    try:
        level = Level.objects.get(id=level_id)
        words = random.sample(level.word.all(), min(level.total_word, level.words))
        data = []
        for w in words:
            data.append({'word': w.word, 'images': w.make_ques, 'audio': w.audio, 'id': w.id, 'answer': -1,
                         'categories': [c.name for c in w.category.all()]})
        return render_to_response('test.html',
                                  RequestContext(request,
                                                 {'fill_active': 1, 'index': [i for i in range(1, len(data) + 1)],
                                                  'data': SafeString(json.dumps(data))}))
    except:
        pass
