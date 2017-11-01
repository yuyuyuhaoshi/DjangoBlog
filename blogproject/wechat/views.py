# coding:utf-8
import hashlib
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.template.loader import render_to_string
from lxml import etree

# Create your views here.

TOKEN = '*******'


def index1(request):
    return HttpResponse(u"nihao!")


def index2(request):
    return HttpResponse(u"index2")


@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        # 获得参数signature nonce token timestamp echostr
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        token = TOKEN

        # 将token、timestamp、nonce字段进行字典顺序排序
        # 然后拼接成一个字符串进行sha1加密
        # 加密后的字符串和signature进行比较，相同则返回echostr。
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()

        hashstr = "%s%s%s" % tuple(tmp_list)
        hashstr = hashlib.sha1(hashstr.encode('utf-8')).hexdigest()

        # sha = hashlib.sha1()
        # hashstr = sha.update("".join(tmp_list)).hexdigest()
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('weixin_index')

    if request.method == 'POST':
        data = smart_str(request.body)
        xml = etree.fromstring(data)
        # 在控制台输出一下挑调试信息
        # print('收到的XML数据')
        # print(data)

        ToUserName = xml.find('ToUserName').text
        FromUserName = xml.find('FromUserName').text
        CreateTime = xml.find('CreateTime').text
        MsgType = xml.find('MsgType').text
        Content = xml.find('Content').text
        MsgId = xml.find('MsgId').text


        time_stamp = str(int(time.time()))
        reply_content = {
            'ToUserName': FromUserName,
            'FromUserName': ToUserName,
            'time': time_stamp,
            'Content': Content,
        }

        response_xml = render_to_string('wechat/wechat_reply.xml', context=reply_content)
        return HttpResponse(response_xml)
