#!/usr/bin/env python
# coding: utf-8

import datetime
import time
import hashlib
import random

import qiniu
import requests

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from util.constants import HTTP_FLAG, CDN_FILES_URL, GET_WORD_AUDIO


def qiniu_token():
    q = qiniu.Auth('P2YzIr4wrfZWlMT_Yqxsj8sf7loXXoHUvyLTwG7n', '91rWvTta-WL9H5bkJG3xM093oOvHDWXeQ8xBspnX')
    token = q.upload_token('longzhuangzhung')
    return token


def qiniu_upload(tmp_file_path):
    token = qiniu_token()
    key = datetime.datetime.now().strftime("%Y/%m/%d/")
    key += hashlib.md5(str(time.time()) + str(random.randint(1111, 9999))).hexdigest()
    ret, info = qiniu.put_file(token, key, tmp_file_path)

    if ret is not None:
        return key
    else:
        return False


def qiniu_upload_by_content(content):
    q = qiniu.Auth('P2YzIr4wrfZWlMT_Yqxsj8sf7loXXoHUvyLTwG7n', '91rWvTta-WL9H5bkJG3xM093oOvHDWXeQ8xBspnX')
    token = q.upload_token('longzhuangzhung')
    now_str = datetime.datetime.now().strftime("%Y/%m/%d/")
    key = "longzhuangzhuang/web/img/%s%s" % (
        now_str, hashlib.md5(str(time.time()) + str(random.randint(1111, 9999))).hexdigest())
    ret, info = qiniu.put_data(token, key, content)

    if ret is not None:
        return key
    else:
        return False


@deconstructible
class AdminStorageToQiniu(Storage):
    def _save(self, name, content):
        try:
            res = qiniu_upload_by_content(content)
        except Exception as e:
            raise
        if res is False:
            return ""
        uri = res
        return uri

    def exists(self, name):
        pass

    def listdir(self, path):
        pass

    def size(self, name):
        return 0

    def url(self, name):
        url = name if HTTP_FLAG in name else "%s%s" % (CDN_FILES_URL, name)
        return url


def get_word_info(word):
    r = requests.get(GET_WORD_AUDIO + word)
    ret = {'pronunciation': '', 'audio': '', 'definition': ''}

    if r.status_code == 200:
        result = r.json()
        if result['status_code'] == 0 and result['msg'] == 'SUCCESS' and 'data' in result:
            data = result['data']
            if 'pronunciation' in data:
                ret['pronunciation'] = data['pronunciation']
            if 'us_audio' in data:
                ret['audio'] = data['us_audio']
            if 'definition' in data:
                ret['definition'] = data['definition']

    return ret
