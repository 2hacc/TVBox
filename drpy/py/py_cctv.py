#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "央视"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"等着我": "TOPC1451378757637200",
			"我爱发明": "TOPC1569314345479107",
			"动物世界": "TOPC1451378967257534",
			"探索发现": "TOPC1451557893544236",
			"创新进行时": "TOPC1570875218228998",
			"我爱发明2021": "TOPC1451557970755294",
			"经典咏流传 第五季":"VIDAIiNbDQzOjE5mLl3T4t2B220403"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		extend['id'] = tid
		extend['p'] = pg
		filterParams = ["id", "p", "d"]
		params = ["", "", ""]
		for idx in range(len(filterParams)):
			fp = filterParams[idx]
			if fp in extend.keys():
				params[idx] = '{0}={1}'.format(filterParams[idx],extend[fp])
		suffix = '&'.join(params)
		url = 'https://api.cntv.cn/NewVideo/getVideoListByColumn?{0}&n=20&sort=desc&mode=0&serviceId=tvcctv&t=json'.format(suffix)
		if not tid.startswith('TOPC'):
			url = 'https://api.cntv.cn/NewVideo/getVideoListByAlbumIdNew?{0}&n=20&sort=desc&mode=0&serviceId=tvcctv&t=json'.format(suffix)
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		vodList = jo['data']['list']
		videos = []
		for vod in vodList:
			guid = vod['guid']
			title = vod['title']
			img = vod['image']
			brief = vod['brief']
			videos.append({
				"vod_id":guid+"###"+img,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		aid = array[0].split('###')
		tid = aid[0]
		url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={0}".format(tid)

		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		title = jo['title'].strip()
		link = jo['hls_url'].strip()
		vod = {
			"vod_id":tid,
			"vod_name":title,
			"vod_pic":aid[1],
			"type_name":'',
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":""
		}
		vod['vod_play_from'] = 'CCTV'
		vod['vod_play_url'] = title+"$"+link

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		rsp = self.fetch(id,headers=self.header)
		content = rsp.text.strip()
		arr = content.split('\n')
		urlPrefix = self.regStr(id,'(http[s]?://[a-zA-z0-9.]+)/')
		url = urlPrefix + arr[-1]
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = ''
		return result

	config = {
		"player": {},
		"filter": {"TOPC1451557970755294": [{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}]}
	}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]