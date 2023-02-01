# coding=utf-8
# !/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import re
import difflib
import urllib

class Spider(Spider):  # 元类 默认的元类 type
    def getName(self):
        return "Alist"

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
            "七米蓝": "https://al.chirmyram.com/",
            "梅花盘": "https://pan.142856.xyz/OneDrive",
            "触光云盘": "https://pan.ichuguang.com",
            # "小孟资源": "https://8023.haohanba.cn/小孟丨资源大合集/无损音乐",
            "资源小站": "https://960303.xyz/ali",
            "轻弹浅唱": "https://g.xiang.lol",
            "小兵组网盘视频": "https://6vv.app"
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
				"type_flag": "1",
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        result = {
            'list': []
        }
        return result

    ver = ''
    baseurl = ''
    def getVersion(self, gtid):
        param = {
            "path": '/'
        }
        if gtid.count('/') == 2:
            gtid = gtid + '/'
        baseurl = re.findall(r"http.*://.*?/", gtid)[0]
        ver = self.fetch(baseurl + 'api/public/settings', param)
        vjo = json.loads(ver.text)['data']
        if type(vjo) is dict:
            ver = 3
        else:
            ver = 2
        self.ver = ver
        self.baseurl = baseurl

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        if tid.count('/') == 2:
            tid = tid + '/'
        nurl = re.findall(r"http.*://.*?/", tid)[0]
        if self.ver == '' or self.baseurl != nurl:
            self.getVersion(tid)
        ver = self.ver
        baseurl = self.baseurl
        if tid.count('/') == 2:
            tid = tid + '/'
        pat = tid.replace(baseurl,"")
        param = {
            "path": '/' + pat
        }
        if ver == 2:
            rsp = self.postJson(baseurl + 'api/public/path', param)
            jo = json.loads(rsp.text)
            vodList = jo['data']['files']
        elif ver == 3:
            rsp = self.postJson(baseurl + 'api/fs/list', param)
            jo = json.loads(rsp.text)
            vodList = jo['data']['content']
        videos = []
        cid = ''
        for vod in vodList:
            if ver == 2:
                img = vod['thumbnail']
            elif ver == 3:
                img = vod['thumb']
            if len(img) == 0:
                if vod['type'] == 1:
                    img = "http://img1.3png.com/281e284a670865a71d91515866552b5f172b.png"
            if pat != '':
                aid = pat + '/'
            else:
                aid = pat
            if vod['type'] == 1:
                tag = "folder"
                remark = "文件夹"
                cid = baseurl + aid + vod['name']
            #计算文件大小
            else:
                size = vod['size']
                if size > 1024 * 1024 * 1024 * 1024.0:
                    fs = "TB"
                    sz = round(size / (1024 * 1024 * 1024 * 1024.0), 2)
                elif size > 1024 * 1024 * 1024.0:
                    fs = "GB"
                    sz = round(size / (1024 * 1024 * 1024.0), 2)
                elif size > 1024 * 1024.0:
                    fs = "MB"
                    sz = round(size / (1024 * 1024.0), 2)
                elif size > 1024.0:
                    fs = "KB"
                    sz = round(size / (1024.0), 2)
                else:
                    fs = "KB"
                    sz = round(size / (1024.0), 2)
                tag = "file"
                remark = str(sz) + fs
                # 开始爬视频与字幕
                srtvodList = str(vodList)
                foldernum = srtvodList.count('\'type\': 1')
                filename = len(vodList) - foldernum
                if filename < 60:
                    if 'mp4' in vod['name'] or 'mkv' in vod['name'] or 'TS' in vod['name'] or 'flv' in vod[
                        'name'] or 'rmvb' in vod['name'] or 'mp3' in vod['name'] or 'flac' in vod['name'] or 'wav' in \
                            vod['name'] or 'wma' in vod['name'] or 'wma' in vod['name']:
                        cid = ''
                        for temvod in vodList:
                            if 'mp4' in temvod['name'] or 'mkv' in temvod['name'] or 'TS' in temvod['name'] or 'flv' in \
                                    temvod['name'] or 'rmvb' in temvod['name'] or 'mp3' in temvod['name'] or 'flac' in \
                                    temvod['name'] or 'wav' in temvod['name'] or 'wma' in temvod['name'] or 'wma' in \
                                    temvod['name']:
                                vurl = baseurl + aid + temvod['name']
                                # 开始爬字幕
                                subname = re.findall(r"(.*)\.", temvod['name'])[0]
                                substr = re.findall(r"\'name\': \'(.*?)\'", str(vodList))
                                if len(substr) == 2:
                                    suball = substr
                                else:
                                    suball = difflib.get_close_matches(subname, substr, len(vodList), cutoff=0.8)
                                for sub in suball:
                                    if sub.endswith(".ass") or sub.endswith(".srt"):
                                        subt = '@@@' + baseurl + aid + sub
                                ifsubt = 'subt' in locals().keys()
                                if ifsubt is False:
                                    cid = cid + '{0}${1}#'.format(temvod['name'], vurl)
                                else:
                                    cid = cid + '{0}${1}{2}#'.format(temvod['name'], vurl, subt)
                            else:
                                cid = cid
                    if cid == '':
                        cid = baseurl + aid + vod['name']
                else:
                    subname = re.findall(r"(.*)\.", vod['name'])[0]
                    substr = re.findall(r"\'name\': \'(.*?)\'", str(vodList))
                    if subname + '.ass' in substr:
                        subt = '@@@' + baseurl + aid + subname + '.ass'
                        cid = baseurl + aid + vod['name'] + subt
                    elif  subname + '.srt' in substr:
                        subt = '@@@' + baseurl + aid + subname + '.srt'
                        cid = baseurl + aid + vod['name'] + subt
                    else:
                        cid = baseurl + aid + vod['name']
            videos.append({
                "vod_id":  cid,
                "vod_name": vod['name'],
                "vod_pic": img,
                "vod_tag": tag,
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = 1
        result['pagecount'] = 1
        result['limit'] = 999
        result['total'] = 999999
        return result

    def detailContent(self, array):
        id = array[0]
        if '$' in id:
            ids = id.split('$')[1].split('#')[0].split('@@@')
            url = ids[0]
        else:
            url = id
        if self.ver == '' or self.baseurl == '':
            self.getVersion(url)
        baseurl = self.baseurl
        if '$' in id:
            vid = re.findall(r"(.*)/", url.replace(baseurl, ""))[0].replace(baseurl, "")
        else:
            vid = url.replace(re.findall(r".*/", url)[0], "")
            id = vid + '$' + id
        vod = {
            "vod_id": vid,
            "vod_name": vid,
            "vod_pic": '',
            "vod_tag": '',
            "vod_play_from": "播放",
            "vod_play_url": id
        }
        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick):
        result = {
            'list': []
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        ifsub = '@@@' in id
        if ifsub is True:
            ids = id.split('@@@')
            if self.ver == '' or self.baseurl == '':
                self.getVersion(ids[1])
            ver = self.ver
            baseurl = self.baseurl
            fileName = ids[1].replace(baseurl, "")
            vfileName = ids[0].replace(baseurl, "")
            param = {
                "path": '/' + fileName,
                "password": "",
                "page_num": 1,
                "page_size": 100
            }
            vparam = {
                "path": '/' + vfileName,
                "password": "",
                "page_num": 1,
                "page_size": 100
            }
            if ver == 2:
                rsp = self.postJson(baseurl + 'api/public/path', param)
                jo = json.loads(rsp.text)
                vodList = jo['data']['files'][0]
                subturl = vodList['url']
                vrsp = self.postJson(baseurl + 'api/public/path', vparam)
                vjo = json.loads(vrsp.text)
                vList = vjo['data']['files'][0]
                url = vList['url']
            elif ver == 3:
                rsp = self.postJson(baseurl + 'api/fs/get', param)
                jo = json.loads(rsp.text)
                vodList = jo['data']
                subturl = vodList['raw_url']
                vrsp = self.postJson(baseurl + 'api/fs/get', vparam)
                vjo = json.loads(vrsp.text)
                vList = vjo['data']
                url = vList['raw_url']
            if subturl.startswith('http') is False:
                head = re.findall(r"h.*?:", baseurl)[0]
                subturl = head + subturl
            if url.startswith('http') is False:
                head = re.findall(r"h.*?:", baseurl)[0]
                url = head + url
            urlfileName = urllib.parse.quote(fileName)
            subturl = subturl.replace(fileName, urlfileName)
            urlvfileName = urllib.parse.quote(vfileName)
            url = url.replace(vfileName, urlvfileName)
            result['subt'] = subturl
        else:
            if self.ver == '' or self.baseurl == '':
                self.getVersion(id)
            ver = self.ver
            baseurl = self.baseurl
            vfileName = id.replace(baseurl, "")
            vparam = {
                "path": '/' + vfileName,
                "password": "",
                "page_num": 1,
                "page_size": 100
            }
            if ver == 2:
                vrsp = self.postJson(baseurl + 'api/public/path', vparam)
                vjo = json.loads(vrsp.text)
                vList = vjo['data']['files'][0]
                driver = vList['driver']
                url = vList['url']
            elif ver == 3:
                vrsp = self.postJson(baseurl + 'api/fs/get', vparam)
                vjo = json.loads(vrsp.text)
                vList = vjo['data']
                url = vList['raw_url']
                driver = vList['provider']
            if url.startswith('http') is False:
                head = re.findall(r"h.*?:", baseurl)[0]
                url = head + url
            urlvfileName = urllib.parse.quote(vfileName)
            url = url.replace(vfileName, urlvfileName)
            if driver == 'Baidu.Disk':
                result["header"] = {"User-Agent": "pan.baidu.com"}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url

        return result

    config = {
        "player": {},
        "filter": {}
    }
    header = {}

    def localProxy(self, param):
        return [200, "video/MP2T", action, ""]