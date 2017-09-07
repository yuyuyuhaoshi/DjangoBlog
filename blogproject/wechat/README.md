# 用Django搭建微信公众号后端
&emsp;&emsp;之前一段时间在公司实习，用的技术栈是PHP+MySQL，主要的工作就是微信相关的开发。然后我也接触到了一些公众号的知识。我对Python特别感兴趣，之前搭建博客的框架是Django，所以突发奇想，看看能不能用Django来做一下后端。搜集了一些资料，百度谷歌了一些，然后就有了这篇东西。
## 微信TOKEN验证
&emsp;&emsp;进入微信公众平台，基本设置会有这样一个服务器配置选项。如果开启就是进入了开发者模式，微信公众平台上自动回复和自定义菜单的功能就会失效。  

![微信公众号设置](http://oqcvxfytp.bkt.clouddn.com/17-9-7/43883103.jpg)
### 创建项目与APP
&emsp;&emsp;我们创建一个Django项目(我这边用的叫blogproject)，创建一个叫'wechat'的app。(关于怎么创建参考[Django的菜鸟教程](http://www.runoob.com/django/django-tutorial.html))。  
&emsp;&emsp;将我们自己创建的APP名称加进去，顺便改一下默认的模板文件夹

```python
# blogproject/setting.py
INSTALLED_APPS = [
    'django.contrib.admin',
    # ...
    # my app
    'wechat',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],# 修改此处
        'APP_DIRS': True,
        # ...
    },
]
```

### 编辑views.py
&emsp;&emsp;来看一下微信的[官方文档](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1445241432)，第1.4小节，有一个案例，可以看到服务器接受signature，timestamp，nonce，echostr这四个参数。  
&emsp;&emsp;我是看了[自强学堂](http://code.ziqiangxuetang.com/django/python-django-weixin.html)的例子，有了下面的代码
```python
# wechat/views.py
# 省略头部引用和声明
TOKEN = '********' # 自己改一下

@csrf_exempt # 关闭csrf验证
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
        # 这个else的作用就是普通的网页打开显示'wx_index'，看看是不是能成功路由(调用)
        else:
            return HttpResponse('weixin_index')
```

### 路由
&emsp;&emsp;光写了函数来处理我们的数据，也不够啊。我总需要去调用他。所以我们需要路由。我们这边的路由分两步进行，先路由到我们的APP，再路由到各个函数。

```python
# blogproject/url.py
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 添加这一行
    url(r'', include('wechat.urls'))
]
```
&emsp;&emsp;然后我们就路由到了我们wechat的APP。接下来在wechat的文件夹下创建一个url.py的文件。  
```python
# wechat/url.py
from django.conf.urls import url
from . import views

app_name = 'wechat'

urlpatterns = [
    url(r'^wechat/index$', views.wechat, name='wechat'),# 这是我们所需要的功能函数
    url(r'^wechat/index1$', views.index1, name='index1'),# 这是测试函数
]
```

### 上传服务器
&emsp;&emsp;我们成功的开启服务后，输入我们的服务器地址或者域名，后面跟上"/wechat/index"，也就是我们正则表达式所匹配到的。

![weixin_index](http://oqcvxfytp.bkt.clouddn.com/17-9-8/23682403.jpg)

出现了weixin_index说明，我们函数的逻辑没有错，接下来就去微信公众号上进行设置啦。按照最上面的那种图填写，出现提交成功就说明我们的设置正确，接下就是对于消息的回复啦！
![提交成功](http://oqcvxfytp.bkt.clouddn.com/17-9-8/530866.jpg)

## 消息回复
&emsp;&emsp;有人会疑惑为什么不用微信官方给的自动回复呢？  
&emsp;&emsp;我想了几个答案：第一呢，用自己的回复更有极(就)客(要)精(装)神(逼)。第二，大家应该都知道一个APP叫SimiSimi，就是那个会聊天的小黄鸡，我要实现这个功能。第三，实现一些查询功能，比如天气，火车票，历史上的今天等等。后两个待添加。这次就完成重复你说话。  
### 消息模板
&emsp;&emsp;我们先来微信回过来的信息，它是一个XML数据包。[微信官方文档](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140453)
```XML
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[this is a test]]></Content>
    <MsgId>1234567890123456</MsgId>
</xml>
```

&emsp;&emsp;微信也给了每个参数的解释    
| 参数      | 描述          |
| ------------- |-------------:|
| ToUserName      | 开发者微信号 |
| FromUserName     | 发送方帐号（一个OpenID）      |
| CreateTime | 消息创建时间 （整型）|
| MsgType | text      |
| Content | 文本消息内容      |
| MsgId | 消息id，64位整型      |
> 注：还有别的类型的xml数据，有需要可以看看官方文档。
### 转化数据
&emsp;&emsp;我接受XML数据，然后将数据转化为Django能处理的数据。
```python
data = smart_str(request.body)
xml = etree.fromstring(data)
```
### 提取数据，并处理
&emsp;&emsp;我们将各个数据内容提取出来
```python
ToUserName = xml.find('ToUserName').text
FromUserName = xml.find('FromUserName').text
CreateTime = xml.find('CreateTime').text
MsgType = xml.find('MsgType').text
Content = xml.find('Content').text
MsgId = xml.find('MsgId').text
```
&emsp;&emsp;我们要考虑这样一个逻辑：  
1. 我们的消息，从哪里来回到哪里去。FromUserName与ToUserName需要对换一下位置。对于我们的服务器来说用户是发送方，所以我们回消息要回给发送方，也就是说发送过去的信息ToUserName=用户的地址。
2. 用户发给我们的服务器什么消息，就回给用户什么信息。Content不变
3. 用户发给我们的消息类型text，我们也不变。
4. 时间不是23:59:59的这种类型，而是一个字符串类型的整型数值。
```python
time_stamp = str(int(time.time()))
reply_content = {
    'ToUserName': FromUserName,
    'FromUserName': ToUserName,
    'time': time_stamp,
    'Content': Content,
}
```
### 创建信息模板
&emsp;&emsp;然后我们创建一个信息模板，叫做'wechat_reply.xml'，放在'templates/wechat'下。当然'templates'与'wechat'文件夹小自己创建。  
&emsp;&emsp;这边的templates文件夹就是在settings.py里修改的目的！  

![目录结构](http://oqcvxfytp.bkt.clouddn.com/17-9-8/78942242.jpg)
```xml
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
</xml>
```
&emsp;&emsp;我们用render_to_string()函数渲染模板信息，并将数据返回给微信。

&emsp;&emsp;最后的代码就是这样：
```python
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
```
### 大功告成！
&emsp;&emsp;提交给我们的服务器，就可以测试啦！  
![](http://oqcvxfytp.bkt.clouddn.com/17-9-8/39394590.jpg)

# END
&emsp;&emsp;写的有一点乱，参考了很多教程，失败了很多次，最主要的原因在token后多加了一个空格。所以这边要注意一下。


&emsp;&emsp;主要是参考了[自强学堂](http://code.ziqiangxuetang.com/django/python-django-weixin.html)和知乎用户[Echo的专栏](https://zhuanlan.zhihu.com/Ehco-python)。他的微信公众号是'翻山越岭breakwall'。

&emsp;&emsp;图片加载不正常可以查看我的博客。