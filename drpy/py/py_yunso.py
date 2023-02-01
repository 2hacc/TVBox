#coding=utf-8
#!/usr/bin/python
import base64
import json
import sys

import requests

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
	def getDependence(self):
		return ['py_ali']
	def getName(self):
		return "py_up云搜"
	def init(self,extend):
		self.ali = extend[0]
		print("============py_pansou============")
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		return result
	def homeVideoContent(self):
		result = {}
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		return result

	def detailContent(self,array):
		tid = array[0]
		print(self.getName())

		pattern = '(https:\\/\\/www.aliyundrive.com\\/s\\/[^\\\"]+)'
		url = self.regStr(tid,pattern)
		print('是这个码',url)

		if len(url) > 0:
			print('阿里')
			return self.ali.detailContent(array)

		


	def searchContent(self,key,quick):
		url = "https://api.upyunso.com/search?keyword={0}&page=1&s_type=2".format(key)
		rsp = requests.get(url=url, headers=self.header)
		vodList = json.loads(base64.b64decode(rsp.text))['result']['items']
		videos = []
		for vod in vodList:

			conList = vod['content']

			for con in conList:
				#print(con)
				pattern = '(https:\\/\\/www.aliyundrive.com\\/s\\/[^\\\"]+)'
				url = self.regStr(con['size'],pattern)


				if len(url)>0:
					vid = con['size']
					videos.append({
						"vod_id": vid,
						"vod_name": con['title'],
						"vod_pic": "https://inews.gtimg.com/newsapp_bt/0/13263837859/1000",
						"vod_remarks": vod['insert_time']
					})
		result = {
			'list':videos
		}
		return result

	def playerContent(self,flag,id,vipFlags):
		return self.ali.playerContent(flag,id,vipFlags)

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]



if __name__ == '__main__':
	a=Spider()
	result=a.searchContent('后天','1')
	print(result)
	print(a.detailContent(['https://www.aliyundrive.com/s/LDwBLChmf4c/folder/6113390cc1df1f8f9c2e498997d308e5099243ae']))