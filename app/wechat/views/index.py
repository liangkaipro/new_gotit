# -*- coding: utf-8 -*-
from .. import wechat
import xml.etree.ElementTree as ET
from ...models import User
from app import db
from flask import request
import time  # 用来记录生成微信消息的时间
import hashlib

'''
一键绑定：系统检测到您已经绑定，无需重复绑定，如果需要更换绑定账号，请先解绑后再进行绑定
绑定界面。
查课表->已绑定进入数据库查课表，未绑定提示未绑定信息，并提示是否不绑定进行查询
查教务成绩
查绩点
查图书借阅情况
解除绑定：系统检测到您已经绑定，是否解除绑定？
系统检测到您并未绑定，所以不需要解绑，前去一键绑定？
使用说明：
'''


def check_if_binding(wechat_id):
    if User.query.filter_by(wechat_id=wechat_id).first():
        return True
    else:
        return False


def cancel_building(wechat_id):
    db.session.delete(User(wechat_id=wechat_id))
    db.session.commit()


@wechat.route('', methods=['GET', 'POST'])  # 微信主页面
def wechat():
    if request.method == 'GET':
        if request.args.get('timestamp') is None:
            return u'对不起，您无权访问此界面'
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        token = 'news_sdut_edu_cn'
        li = sorted([token, timestamp, nonce])
        sha1 = hashlib.sha1()
        map(sha1.update, li)
        hashcode = sha1.hexdigest()
        if hashcode == request.args.get('signature'):
            return echostr
        else:
            print("There is an error")
    elif request.method == 'POST':
        message = request.data  # 接收用户消息
        root = ET.fromstring(message)  # 解析xml
        to_user_name = root.findall('ToUserName')[0].text  # 开发者账号
        from_user_name = root.findall('FromUserName')[0].text  # 用户微信id
        create_time = root.findall('CreateTime')[0].text  # 消息创建时间 （整型）
        message_type = root.findall('MsgType')[0].text  # 消息类型text
        content = root.findall('Content')[0].text  # 消息内容
        message_id = root.findall('MsgId')[0].text  # 消息的ID
        if content == u"一键绑定":
            if check_if_binding(from_user_name):  # 已经绑定的话返回的是true提示用户不需要再绑定了
                create_time = int(round(time.time() * 1000))
                return """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[系统检测到您已经绑定，无需重复绑定，如果需要更换绑定账号，请先解绑后再进行绑定]]></Content>
                </xml>""" % (from_user_name, to_user_name, create_time)
            else:  # 用户没有绑定的话进入绑定界面，返回的图文消息
                create_time = int(round(time.time() * 1000))
                return """
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统]]></Title>
                <Description><![CDATA[系统检测到您并未绑定，点击此页面前去绑定。]]></Description>
                <Url><![CDATA[lvhuiyang.cn/wechat/building/zhengfang?token=huiyang2333&wechat_id=%s]]></Url>
                </item>
                </xml>
                """ % (from_user_name, to_user_name, create_time, from_user_name)
        elif content == u"查课表":
            if check_if_binding(from_user_name):

                return """
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>1</ArticleCount>
                    <Articles>
                    <item>
                    <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统，课表查询]]></Title>
                    <Description><![CDATA[>>> 查看详细信息 <<<]]></Description>
                    <Url><![CDATA[lvhuiyang.cn/wechat/class?wechat_id=%s]]></Url>
                    </item>
                    </xml>
                    """ % (from_user_name, to_user_name, create_time, from_user_name)
            else:
                return """
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统]]></Title>
                <Description><![CDATA[系统检测到您并未绑定，点击此页面前去绑定。或者您并不想进行绑定，请点击菜单栏的‘无绑定查询’]]></Description>
                <Url><![CDATA[lvhuiyang.cn/wechat/building/zhengfang?token=huiyang2333&wechat_id=%s]]></Url>
                </item>
                </xml>
                """ % (from_user_name, to_user_name, create_time, from_user_name)
            pass
        elif content == u"查教务成绩":
            if check_if_binding(from_user_name):

                return """
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>1</ArticleCount>
                    <Articles>
                    <item>
                    <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统，教务处查询]]></Title>
                    <Description><![CDATA[>>> 查看详细信息 <<<]]></Description>
                    <Url><![CDATA[lvhuiyang.cn/wechat/zhengfang?wechat_id=%s]]></Url>
                    </item>
                    </xml>
                    """ % (from_user_name, to_user_name, create_time, from_user_name)
            else:
                return """
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统]]></Title>
                <Description><![CDATA[系统检测到您并未绑定，点击此页面前去绑定。]]></Description>
                <Url><![CDATA[lvhuiyang.cn/wechat/building/zhengfang?token=huiyang2333&wechat_id=%s]]></Url>
                </item>
                </xml>
                """ % (from_user_name, to_user_name, create_time, from_user_name)
            pass
        elif content == u"查绩点":
            if check_if_binding(from_user_name):

                return """
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>1</ArticleCount>
                    <Articles>
                    <item>
                    <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统，综合成绩以及绩点查询]]></Title>
                    <Description><![CDATA[>>> 查看详细信息 <<<]]></Description>
                    <Url><![CDATA[lvhuiyang.cn/wechat/jwc?wechat_id=%s]]></Url>
                    </item>
                    </xml>
                    """ % (from_user_name, to_user_name, create_time, from_user_name)
            else:
                return """
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统]]></Title>
                <Description><![CDATA[系统检测到您并未绑定，点击此页面前去绑定。]]></Description>
                <Url><![CDATA[lvhuiyang.cn/wechat/building/zhengfang?token=huiyang2333&wechat_id=%s]]></Url>
                </item>
                </xml>
                """ % (from_user_name, to_user_name, create_time, from_user_name)

        elif content == u"图书借阅查询":
            if check_if_binding(from_user_name):

                return """
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>1</ArticleCount>
                    <Articles>
                    <item>
                    <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统，图书借阅查询]]></Title>
                    <Description><![CDATA[>>> 查看详细信息 <<<]]></Description>
                    <Url><![CDATA[lvhuiyang.cn/wechat/library?wechat_id=%s]]></Url>
                    </item>
                    </xml>
                    """ % (from_user_name, to_user_name, create_time, from_user_name)
            else:
                return """
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[欢迎使用山东理工大学报教务信息查询系统]]></Title>
                <Description><![CDATA[系统检测到您并未绑定，点击此页面前去绑定。]]></Description>
                <Url><![CDATA[lvhuiyang.cn/wechat/building/zhengfang?token=huiyang2333&wechat_id=%s]]></Url>
                </item>
                </xml>
                """ % (from_user_name, to_user_name, create_time, from_user_name)
        elif content == u"解除绑定":
            if check_if_binding(from_user_name):
                cancel_building(from_user_name)
                return """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[解绑成功，您可以再次绑定。]]></Content>
                </xml>""" % (from_user_name, to_user_name, create_time)
            else:
                return """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[系统检测到您并没有绑定，所以无需进行此操作。]]></Content>
                </xml>""" % (from_user_name, to_user_name, create_time)
        else:
            return u"请求非法"
    else:
        return u"请求非法"
