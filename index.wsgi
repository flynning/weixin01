#coding: utf-8  
import os  
import hashlib  
  
import sae  
#需要的第三方库  
import web  
from lxml import etree  
  
#TOKEN 到微信公众平台自己设置  
config={  
    "WEIXIN": 'weixin'}  
          
urls = (  
    '/weixin', 'weixin'  
)  
  
app_root = os.path.dirname(__file__)  
  
class weixin:          
    #GET方法，主要用来注册url  
    def GET(self):  
        data = web.input()  
        #以下是微信公众平台请求的参数  
        signature = data.signature  
        timestamp = data.timestamp  
        nonce = data.nonce  
        echostr = data.echostr  
  
        #自己定义的 TOKEN  
        token = 'input your taken'  
          
        #对微信发送的请求，做验证  
        tmplist = [ token, timestamp, nonce ]  
        #tmplist.sort()  
        tmplist.sort()  
        tmpstr = ''.join( tmplist )  
        hashstr = hashlib.sha1( tmpstr ).hexdigest()  
  
        #如果相等，返回验证信息  
        if hashstr == signature:  
            return echostr  
          
        #如果不相等，返回错误，并打印调试信息  
        print signature,timestamp,nonce  
        print tmpstr,hashstr  
        return 'Error' + echostr  
  
  
    def POST(self):  
        #接收微信的请求内容  
        data = web.data()  
        #解析XML内容  
        root = etree.fromstring( data )  
        child = list( root )  
        recv = {}  
        for i in child:  
            recv[i.tag] = i.text  
  
        #print data  
        #print recv  
          
        #测试demo 所以接收到啥内容，就原样返回  
        textTpl = """<xml> 
            <ToUserName><![CDATA[%s]]></ToUserName> 
            <FromUserName><![CDATA[%s]]></FromUserName> 
            <CreateTime>%s</CreateTime> 
            <MsgType><![CDATA[%s]]></MsgType> 
            <Content><![CDATA[%s]]></Content> 
            <FuncFlag>0</FuncFlag> 
            </xml>"""  
        echostr = textTpl % (recv['FromUserName'], recv['ToUserName'],recv['CreateTime'],recv['MsgType'],recv['Content'])  
        return echostr  
  
app = web.application(urls, globals()).wsgifunc()  
  
application = sae.create_wsgi_app(app)  