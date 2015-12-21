# -*-coding:utf-8-*-
from settings import *
MENU = """
{
    "button": [
        {
            "type": "view",
            "name": "个人信息",
            "url": "%s"
        },
        {
            "name": "健康功能",
            "sub_button": [
                {
                    "type": "click",
                    "name": "看步数",
                    "key": "STEP_COUNT"
                },
                {
                    "type": "view",
                    "name": "时间线",
                    "url": "%s"
                }
                {
                    "type": "click",
                    "name": "排行榜",
                    "key": "RANK_LIST"
                },
                {
                    "type": "click",
                    "name": "数据报表",
                    "key": "CHART"
                }
            ]
        },
        {
            "name": "玩玩游戏",
            "sub_button": [
                {
                    "type": "click",
                    "name": "2048",
                    "key": "2048"
                },
                {
                    "type": "click",
                    "name": "fp_bird",
                    "key": "FLAPPY"
                },
                {
                    "type": "view",
                    "name": "龙虎榜",
                    "url": "%s"
                }
            ]
        }
    ]
}
"""


USER_URL='https://open.weixin.qq.com/connect/oauth2/authorize?appid='+AppID+'&redirect_uri=http%3a%2f%2f'+LOCAL_IP+'%2fregister.html'+'&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
RANK_URL='https://open.weixin.qq.com/connect/oauth2/authorize?appid='+AppID+'&redirect_uri=http%3a%2f%2f'+LOCAL_IP+'%2frank.html'+'&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
TIME_URL='https://open.weixin.qq.com/connect/oauth2/authorize?appid='+AppID+'&redirect_uri=http%3a%2f%2f'+LOCAL_IP+'%2frank.html'+'&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'