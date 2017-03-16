# !/usr/bin/env python
# coding: utf-8
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext


def login(request):
    if request.method == 'GET':
        return render_to_response('login.html',
                                  RequestContext(request))
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next = request.GET.get('next', '/')
        if not username or not password:
            return render_to_response('login.html', RequestContext(request, {'error': u'请输入用户名和密码'}))

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            request.session.set_expiry(0)  # 用户关闭浏览器session就会失效
            return HttpResponseRedirect(next)
        else:
            return render_to_response('login.html', RequestContext(request, {'error': u'用户名密码错误'}))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')


def register(request):
    if request.method == 'GET':
        return render_to_response('register.html',
                                  RequestContext(request))
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        retypepassword = request.POST.get('retypepassword', '')
        if not username or not password:
            return render_to_response('register.html', RequestContext(request, {'error': u'请输入用户名和密码'}))
        elif password != retypepassword:
            return render_to_response('register.html', RequestContext(request, {'error': u'两次输入的密码不一致，请确认'}))

        filterResult = User.objects.filter(username=username)
        if len(filterResult) > 0:
            newname = u'用户名已存在，试试' + username + str(len(filterResult))
            return render_to_response('register.html',
                                      RequestContext(request, {'error': newname}))

        user = User()  # d************************
        user.username = username
        user.set_password(password)
        # user.email = email
        user.save()
        return HttpResponseRedirect('/accounts/login/')


def forgot(request):
    if request.method == 'GET':
        return render_to_response('forgot.html',
                                  RequestContext(request))
    else:
        return render_to_response('forgot.html',
                                  RequestContext(request, {'error': u'您输入的用户名不存在'}))
