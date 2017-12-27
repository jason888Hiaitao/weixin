from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from django.utils.encoding import smart_str
from wechatpy import parse_message
from django.views.decorators.csrf import csrf_exempt
from wechatpy.replies import TextReply

WEIXIN_TOKEN='token'

def index(res):
    return HttpResponse(u'欢迎来到Django')

@csrf_exempt
def weixinCheck(request):
    '''
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    :param request: 
    :return: 
    '''
    if request.method=='GET':
        signature = request.GET.get("signature",None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        print('进来了')
        try:
            check_signature(token, signature, timestamp, nonce)
            return HttpResponse(
                request.GET.get('echostr', ''), content_type="text/plain")
        except InvalidSignatureException:
         # 处理异常情况或忽略
         print('验证失败')
    elif request.method=='POST':
        xml_message = smart_str(request.body)
        msg = parse_message(xml_message)
        reply = TextReply(content='你好，这是测试', message=msg)
        xml_respose = reply.render()
        return HttpResponse(xml_respose,content_type="application/xml")




