# !/usr/bin/env python
# coding: utf-8
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
import random

# Create your views here.
from django.template import RequestContext
from django.template.defaultfilters import register
from django.utils.safestring import SafeString

from testing.models import Level, Paper, Question, Word


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
    if request.method == 'GET':
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
    else:
        data = request.POST.get('data', '')
        if not data:
            return JsonResponse({"msg": "error", "data": "para error"})
        else:
            res = json.loads(data)
            paper = Paper()
            paper.user = request.user
            paper.level = Level.objects.get(id=level_id)
            paper.score = 0
            paper.time = 0
            paper.save()
            success = 0
            total = 0
            for qa in res:
                total += 1
                question = Question()
                question.word = Word.objects.get(id=qa['id'])
                if qa['answer'] == qa['images']['result']:
                    question.result = 1
                    success += 1
                else:
                    question.result = 0
                question.save()
                paper.questions.add(question)
            paper.score = int(success * 100 / total)
            paper.save()
            return JsonResponse({"msg": "success", "data": "perfect"})
