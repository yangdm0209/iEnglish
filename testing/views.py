# !/usr/bin/env python
# coding: utf-8
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
import random

# Create your views here.
from django.template import RequestContext
from django.utils.safestring import SafeString

from testing.models import Level, Paper, Question, Word


def main(request):
    return HttpResponseRedirect('/know/')


@login_required
def know(request):
    levels = Level.objects.all()
    return render_to_response('know.html',
                              RequestContext(request, {'know_active': 1, 'levels': levels}))


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
                                                      'data': SafeString(json.dumps(data)), 'know_active': 1}))
        except:
            return render_to_response('error.html', RequestContext(request, {'error': '生成试题错误，请稍后再试'}))
    else:
        data = request.POST.get('data', '')
        if not data:
            return render_to_response('error.html', RequestContext(request, {'error': '怎么没有data参数'}))
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
            return HttpResponseRedirect('/know/test/report/%d' % paper.id)


def report(request, paperid):
    try:
        data = {}
        paper = Paper.objects.get(id=paperid)
        words = paper.questions.all()
        for que in paper.questions.all():
            for tag in [c.name for c in que.word.category.all()]:
                if tag not in data:
                    data[tag] = {'count': 1, 'result': 0}
                else:
                    data[tag]['count'] += 1
                if que.result:
                    data[tag]['result'] += 1
        tags = []
        count = []
        result = []
        for key in data:
            tags.append(key)
            count.append(data[key]['count'])
            result.append(data[key]['result'])

        return render_to_response('report.html',
                                  RequestContext(request, {'username': paper.username, 'score': paper.score,
                                                           'level': paper.levelname, 'created': paper.date,
                                                           'words': words, 'tags': tags, 'count': count,
                                                           'result': result, 'know_active': 1}))
    except:
        return render_to_response('error.html', RequestContext(request, {'error': '您所查找的测试结果不存在'}))


def list(request, levelid):
    try:
        level = Level.objects.get(id=levelid)
        papers = Paper.objects.filter(level=levelid)
        list = []
        for p in papers:
            list.append({'id': p.id, 'user': p.username, 'score': p.score, 'date': p.date})
        return render_to_response('list.html',
                                  RequestContext(request, {'know_active': 1, 'list': list, 'level': level.name,
                                                           'count': len(papers)}))
    except:
        return render_to_response('error.html', RequestContext(request, {'error': '您所查找的测试结果不存在'}))
