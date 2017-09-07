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

TOKEN = 'yuhaoshi'


def index1(request):
    return HttpResponse(u"nihao!")


def index2(request):
    return HttpResponse(u"index2")


@csrf_exempt
def wechat(request):
    # return HttpResponse('wx_index')
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        token = TOKEN

        # 按照微信的验证要求将token、timestamp、nonce字段进行字典顺序排序
        # 将三个参数字符串拼接成一个字符串进行sha1加密
        # 获得加密后的字符串可与signature对比，标识该请求来源于微信
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        # sha = hashlib.sha1()
        # hashstr = sha.update("".join(tmp_list)).hexdigest()
        hashstr = "%s%s%s" % tuple(tmp_list)
        hashstr = hashlib.sha1(hashstr.encode('utf-8')).hexdigest()
        # hashstr = ''.join([s for s in tmp_list])
        #
        # # 通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
        # hashstr = hashlib.sha1(hashstr).hexdigest()

        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('wx_index1')

    if request.method == 'POST':
        data = smart_str(request.body)
        xml = etree.fromstring(data)
        # 在控制台输出一下挑调试信息
        # print('**********收到的XML***********')
        # print(data)

        ToUserName = xml.find('ToUserName').text
        FromUserName = xml.find('FromUserName').text
        CreateTime = xml.find('CreateTime').text
        MsgType = xml.find('MsgType').text
        Content = xml.find('Content').text
        MsgId = xml.find('MsgId').text
        # Content= "nihao"


        time_stamp = str(int(time.time()))
        reply_content = {
            'ToUserName': FromUserName,
            'FromUserName': ToUserName,
            'time': time_stamp,
            'Content': Content,
        }
        xml = """
            <xml>
                <ToUserName>
                    <![CDATA[{{ ToUserName }}]]>
                </ToUserName>
                <FromUserName>
                    <![CDATA[{{ FromUserName }}]]>
                </FromUserName>
                <CreateTime>{{ time }}</CreateTime>
                <MsgType>
                    <![CDATA[text]]>
                </MsgType>
                <Content>
                    <![CDATA[{{ Content }}]]>
                </Content>
            </xml>"""

        response_xml = render_to_string('wechat/wechat_reply.xml', context=reply_content)
        return HttpResponse(response_xml)
