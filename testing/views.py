# !/usr/bin/env python
# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext


@login_required
def main(request):
    return render_to_response('main.html',
                              RequestContext(request))


def test(request, level_id):
    print level_id
    return render_to_response('test.html',
                              RequestContext(request))