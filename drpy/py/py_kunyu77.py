#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):
	def getName(self):
		return "77"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def homeContent(self,filter):
		result = {}
		url = 'http://api.kunyu77.com/api.php/provide/filter'
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		classes = []
		jData = jo['data']
		for cKey in jData.keys():
			classes.append({
				'type_name':jData[cKey][0]['cat'],
				'type_id':cKey
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']	
		return result
	def homeVideoContent(self):
		url = 'http://api.kunyu77.com/api.php/provide/homeBlock?type_id=0'
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		blockList = jo['data']['blocks']
		videos = []
		for block in blockList:
			vodList = block['contents']
			for vod in vodList:
				videos.append({
					"vod_id":vod['id'],
					"vod_name":vod['title'],
					"vod_pic":vod['videoCover'],
					"vod_remarks":vod['msg']
				})
		result = {
			'list':videos
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		if 'type_id' not in extend.keys():
			extend['type_id'] = tid
		extend['pagenum'] = pg
		filterParams = ["type_id", "pagenum"]
		params = ["", ""]
		for idx in range(len(filterParams)):
			fp = filterParams[idx]
			if fp in extend.keys():
				params[idx] = '&'+filterParams[idx]+'='+extend[fp]
		suffix = ''.join(params)
		url = 'http://api.kunyu77.com/api.php/provide/searchFilter?pagesize=24{0}'.format(suffix)
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		vodList = jo['data']['result']
		videos = []
		for vod in vodList:
			videos.append({
				"vod_id":vod['id'],
				"vod_name":vod['title'],
				"vod_pic":vod['videoCover'],
				"vod_remarks":vod['msg']
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		tid = array[0]
		url = 'http://api.kunyu77.com/api.php/provide/videoDetail?devid=453CA5D864457C7DB4D0EAA93DE96E66&package=com.sevenVideo.app.android&version=1.8.7&ids={0}'.format(tid)
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		node = jo['data']
		vod = {
			"vod_id":node['id'],
			"vod_name":node['videoName'],
			"vod_pic":node['videoCover'],
			"type_name":node['subCategory'],
			"vod_year":node['year'],
			"vod_area":node['area'],
			"vod_remarks":node['msg'],
			"vod_actor":node['actor'],
			"vod_director":node['director'],
			"vod_content":node['brief'].strip()
		}
		listUrl = 'http://api.kunyu77.com/api.php/provide/videoPlaylist?devid=453CA5D864457C7DB4D0EAA93DE96E66&package=com.sevenVideo.app.android&version=1.8.7&ids={0}'.format(tid)
		listRsp = self.fetch(listUrl,headers=self.header)
		listJo = json.loads(listRsp.text)
		playMap = {}
		episodes = listJo['data']['episodes']
		for ep in episodes:
			playurls = ep['playurls']
			for playurl in playurls:
				source = playurl['playfrom']
				if source not in playMap.keys():
					playMap[source] = []
				playMap[source].append(playurl['title'].strip() + '$' + playurl['playurl'])

		playFrom = []
		playList = []
		for key in playMap.keys():
			playFrom.append(key)
			playList.append('#'.join(playMap[key]))

		vod_play_from = '$$$'
		vod_play_from = vod_play_from.join(playFrom)
		vod_play_url = '$$$'
		vod_play_url = vod_play_url.join(playList)
		vod['vod_play_from'] = vod_play_from
		vod['vod_play_url'] = vod_play_url

		result = {
			'list':[
				vod
			]
		}
		return result

	def searchContent(self,key,quick):		
		url = 'http://api.kunyu77.com/api.php/provide/searchVideo?searchName={0}'.format(key)
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		vodList = jo['data']
		videos = []
		for vod in vodList:
			videos.append({
				"vod_id":vod['id'],
				"vod_name":vod['videoName'],
				"vod_pic":vod['videoCover'],
				"vod_remarks":vod['msg']
			})
		result = {
			'list':videos
		}
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {
		"User-Agent":"okhttp/3.12.0"
	}
	def playerContent(self,flag,id,vipFlags):
		result = {}
		url = 'http://api.kunyu77.com/api.php/provide/parserUrl?url={0}'.format(id)
		jo = self.fetch(url,headers=self.header).json()
		result = {
			'parse':0,
			'jx':0,
			'playUrl':'',
			'url':id,
			'header':''
		}
		if flag in vipFlags:
			result['parse'] = 1
			result['jx'] = 1
		return result
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]