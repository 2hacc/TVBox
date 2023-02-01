# coding=utf-8
# !/usr/bin/python
import sys

sys.path.append('..')
from base.spider import Spider
import json
from requests import session, utils
import os
import time
import base64


class Spider(Spider):  # 元类 默认的元类 type
    def getName(self):
        return "哔哩影视"

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "番剧": "1",
            "国创": "4",
            "电影": "2",
            "电视剧": "5",
            "纪录片": "3",
            "综艺": "7",
            "全部": "全部",
            "追番": "追番",
            "追剧": "追剧",
            "时间表": "时间表",

        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    cookies = ''
    userid = ''

    def getCookie(self):
        # --------↓↓↓↓↓↓↓------在下方cookies_str后的双引号内填写-------↓↓↓↓↓↓↓--------
        cookies_str = ""
        if cookies_str:
            cookies = dict([co.strip().split('=', 1) for co in cookies_str.split(';')])
            bili_jct = cookies['bili_jct']
            SESSDATA = cookies['SESSDATA']
            DedeUserID = cookies['DedeUserID']
            cookies_jar = {"bili_jct": bili_jct,
                           'SESSDATA': SESSDATA,
                           'DedeUserID': DedeUserID
                           }
            rsp = session()
            rsp.cookies = cookies_jar
            content = self.fetch("https://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
            res = json.loads(content.text)
            if res["code"] == 0:
                self.cookies = rsp.cookies
                self.userid = res["data"].get('mid')
                return rsp.cookies
        rsp = self.fetch("https://www.bilibili.com/")
        self.cookies = rsp.cookies
        return rsp.cookies

    # 将超过10000的数字换成成以万和亿为单位
    def zh(self, num):
        if int(num) >= 100000000:
            p = round(float(num) / float(100000000), 1)
            p = str(p) + '亿'
        else:
            if int(num) >= 10000:
                p = round(float(num) / float(10000), 1)
                p = str(p) + '万'
            else:
                p = str(num)
        return p

    def homeVideoContent(self):
        result = {}
        videos = self.get_rank(1)['list'][0:5]
        for i in [4, 2, 5, 3, 7]:
            videos += self.get_rank2(i)['list'][0:5]
        result['list'] = videos
        return result

    def get_rank(self, tid):
        result = {}
        url = 'https://api.bilibili.com/pgc/web/rank/list?season_type={0}&day=3'.format(tid)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['result']['list']
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['cover'].strip()
                remark = vod['new_ep']['index_show']
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_rank2(self, tid):
        result = {}
        url = 'https://api.bilibili.com/pgc/season/rank/web/list?season_type={0}&day=3'.format(tid)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['cover'].strip()
                remark = vod['new_ep']['index_show']
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_zhui(self, pg, mode):
        result = {}
        if len(self.cookies) <= 0:
            self.getCookie()
        url = 'https://api.bilibili.com/x/space/bangumi/follow/list?type={2}&follow_status=0&pn={1}&ps=10&vmid={0}'.format(self.userid, pg, mode)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['list']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = vod['title']
            img = vod['cover'].strip()
            remark = vod['new_ep']['index_show'].strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def get_all(self, tid, pg, order, season_status, extend):
        result = {}
        if len(self.cookies) <= 0:
            self.getCookie()
        url = 'https://api.bilibili.com/pgc/season/index/result?order={2}&pagesize=20&type=1&season_type={0}&page={1}&season_status={3}'.format(tid, pg, order, season_status)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['list']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = vod['title']
            img = vod['cover'].strip()
            remark = vod['index_show'].strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def get_timeline(self, tid, pg):
        result = {}
        url = 'https://api.bilibili.com/pgc/web/timeline/v2?season_type={0}&day_before=2&day_after=4'.format(tid)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos1 = []
            vodList = jo['result']['latest']
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['cover'].strip()
                remark = vod['pub_index'] + '　' + vod['follows'].replace('系列', '')
                videos1.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            videos2 = []
            for i in range(0, 7):
                vodList = jo['result']['timeline'][i]['episodes']
                for vod in vodList:
                    if str(vod['published']) == "0":
                        aid = str(vod['season_id']).strip()
                        title = str(vod['title']).strip()
                        img = str(vod['cover']).strip()
                        date = str(time.strftime("%m-%d %H:%M", time.localtime(vod['pub_ts'])))
                        remark = date + "   " + vod['pub_index']
                        videos2.append({
                            "vod_id": aid,
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": remark
                        })
            result['list'] = videos2 + videos1
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        if len(self.cookies) <= 0:
            self.getCookie()
        if tid == "1":
            return self.get_rank(tid=tid)
        elif tid in {"2", "3", "4", "5", "7"}:
            return self.get_rank2(tid=tid)
        elif tid == "全部":
            tid = '1'    # 全部界面默认展示最多播放的番剧
            order = '2'
            season_status = '-1'
            if 'tid' in extend:
                tid = extend['tid']
            if 'order' in extend:
                order = extend['order']
            if 'season_status' in extend:
                season_status = extend['season_status']
            return self.get_all(tid, pg, order, season_status, extend)
        elif tid == "追番":
            return self.get_zhui(pg, 1)
        elif tid == "追剧":
            return self.get_zhui(pg, 2)
        elif tid == "时间表":
            tid = 1
            if 'tid' in extend:
                tid = extend['tid']
            return self.get_timeline(tid, pg)
        else:
            result = self.searchContent(key=tid,  quick="false")
        return result

    def cleanSpace(self, str):
        return str.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    def detailContent(self, array):
        aid = array[0]
        url = "https://api.bilibili.com/pgc/view/web/season?season_id={0}".format(aid)
        rsp = self.fetch(url, headers=self.header)
        jRoot = json.loads(rsp.text)
        jo = jRoot['result']
        id = jo['season_id']
        title = jo['title']
        pic = jo['cover']
        # areas = jo['areas']['name']  改bilidanmu显示弹幕
        typeName = jo['share_sub_title']
        date = jo['publish']['pub_time'][0:4]
        dec = jo['evaluate']
        remark = jo['new_ep']['desc']
        stat = jo['stat']
        # 演员和导演框展示视频状态，包括以下内容：
        status = "弹幕: " + self.zh(stat['danmakus']) + "　点赞: " + self.zh(stat['likes']) + "　投币: " + self.zh(
            stat['coins']) + "　追番追剧: " + self.zh(stat['favorites'])
        if 'rating' in jo:
            score = "评分: " + str(jo['rating']['score']) + '　' + jo['subtitle']
        else:
            score = "暂无评分" + '　' + jo['subtitle']
        vod = {
            "vod_id": id,
            "vod_name": title,
            "vod_pic": pic,
            "type_name": typeName,
            "vod_year": date,
            "vod_area": "bilidanmu",
            "vod_remarks": remark,
            "vod_actor": status,
            "vod_director": score,
            "vod_content": dec
        }
        ja = jo['episodes']
        playUrl = ''
        for tmpJo in ja:
            eid = tmpJo['id']
            cid = tmpJo['cid']
            part = tmpJo['title'].replace("#", "-")
            playUrl = playUrl + '{0}${1}_{2}#'.format(part, eid, cid)

        vod['vod_play_from'] = 'B站'
        vod['vod_play_url'] = playUrl

        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick):
        if len(self.cookies) <= 0:
            self.getCookie()
        url1 = 'https://api.bilibili.com/x/web-interface/search/type?search_type=media_bangumi&keyword={0}'.format(
            key)  # 番剧搜索
        rsp1 = self.fetch(url1, cookies=self.cookies)
        content1 = rsp1.text
        jo1 = json.loads(content1)
        rs1 = jo1['data']
        url2 = 'https://api.bilibili.com/x/web-interface/search/type?search_type=media_ft&keyword={0}'.format(
            key)  # 影视搜索
        rsp2 = self.fetch(url2, cookies=self.cookies)
        content2 = rsp2.text
        jo2 = json.loads(content2)
        rs2 = jo2['data']
        videos = []
        if rs1['numResults'] == 0:
            vodList = jo2['data']['result']
        elif rs2['numResults'] == 0:
            vodList = jo1['data']['result']
        else:
            vodList = jo1['data']['result'] + jo2['data']['result']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = key + '➢' + vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
            img = vod['cover'].strip()  # vod['eps'][0]['cover'].strip()原来的错误写法
            remark = vod['index_show']
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        result = {
            'list': videos
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        ids = id.split("_")
        header = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        url = 'https://api.bilibili.com/pgc/player/web/playurl?qn=116&ep_id={0}&cid={1}'.format(ids[0], ids[1])
        if len(self.cookies) <= 0:
            self.getCookie()
        rsp = self.fetch(url, cookies=self.cookies, headers=header)
        jRoot = json.loads(rsp.text)
        if jRoot['message'] != 'success':
            print("需要大会员权限才能观看")
            return {}
        jo = jRoot['result']
        ja = jo['durl']
        maxSize = -1
        position = -1
        for i in range(len(ja)):
            tmpJo = ja[i]
            if maxSize < int(tmpJo['size']):
                maxSize = int(tmpJo['size'])
                position = i

        url = ''
        if len(ja) > 0:
            if position == -1:
                position = 0
            url = ja[position]['url']

        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        result["contentType"] = 'video/x-flv'
        return result

    config = {
        "player": {},
        "filter": {
            "全部": [
                {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "番剧",
                        "v": "1"
                    },
                        {
                            "n": "国创",
                            "v": "4"
                        },

                        {
                            "n": "电影",
                            "v": "2"
                        },
                        {
                            "n": "电视剧",
                            "v": "5"
                        },
                        {
                            "n": "记录片",
                            "v": "3"
                        },
                        {
                            "n": "综艺",
                            "v": "7"
                        }

                    ]
                },
                {
                    "key": "order",
                    "name": "排序",
                    "value": [

                        {
                            "n": "播放数量",
                            "v": "2"
                        },

                        {
                            "n": "更新时间",
                            "v": "0"
                        },

                        {
                            "n": "最高评分",
                            "v": "4"
                        },
                        {
                            "n": "弹幕数量",
                            "v": "1"
                        },
                        {
                            "n": "追看人数",
                            "v": "3"
                        },

                        {
                            "n": "开播时间",
                            "v": "5"
                        },
                        {
                            "n": "上映时间",
                            "v": "6"
                        },

                    ]
                },
                {
                    "key": "season_status",
                    "name": "付费",
                    "value": [
                        {
                            "n": "全部",
                            "v": "-1"
                        },
                        {
                            "n": "免费",
                            "v": "1"
                        },

                        {
                            "n": "付费",
                            "v": "2%2C6"
                        },

                        {
                            "n": "大会员",
                            "v": "4%2C6"
                        },

                    ]
                },
            ],


            "时间表": [{
                "key": "tid",
                "name": "分类",
                "value": [

                    {
                        "n": "番剧",
                        "v": "1"
                    },

                    {
                        "n": "国创",
                        "v": "4"
                    },

                ]
            },
            ],
        }
    }


    header = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def localProxy(self, param):
        return [200, "video/MP2T", action, ""]
