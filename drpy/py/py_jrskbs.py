#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import re
import math

class Spider(Spider):
	def getName(self):
		return "体育直播"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"全部": ""
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
	def homeVideoContent(self):
		result = {}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'https://m.jrskbs.com'
		rsp = self.fetch(url)
		html = self.html(rsp.text)
		aList = html.xpath("//div[contains(@class, 'contentList')]/a")
		videos = []
		numvL = len(aList)
		pgc = math.ceil(numvL/15)
		for a in aList:
			aid = a.xpath("./@href")[0]
			aid = self.regStr(reg=r'/live/(.*?).html', src=aid)
			img = a.xpath(".//div[@class='contentLeft']/p/img/@src")[0]
			home = a.xpath(".//div[@class='contentLeft']/p[@class='false false']/text()")[0]
			away = a.xpath(".//div[@class='contentRight']/p[@class='false false']/text()")[0]
			rmList = a.xpath(".//div[@class='contentCenter']/p/text()")
			remark = rmList[1].replace('|','').replace(' ','') + '|' + rmList[0]
			videos.append({
				"vod_id": aid,
				"vod_name": home + 'vs' + away,
				"vod_pic": img,
				"vod_remarks": remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = pgc
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		aid = array[0]
		url = "http://m.jrskbs.com/live/{0}.html".format(aid)
		rsp = self.fetch(url)
		root = self.html(rsp.text)
		divContent = root.xpath("//div[@class='today']")[0]
		home = divContent.xpath(".//p[@class='onePlayer homeTeam']/text()")[0]
		away = divContent.xpath(".//div[3]/text()")[0].strip()
		title = home + 'vs' + away
		pic = divContent.xpath(".//img[@class='gameLogo1 homeTeam_img']/@src")[0]
		typeName = divContent.xpath(".//div/p[@class='name1 matchTime_wap']/text()")[0]
		remark = divContent.xpath(".//div/p[@class='time1 matchTitle']/text()")[0].replace(' ','')
		vod = {
			"vod_id": aid,
			"vod_name": title,
			"vod_pic": pic,
			"type_name": typeName,
			"vod_year": "",
			"vod_area": "",
			"vod_remarks": remark,
			"vod_actor": '',
			"vod_director":'',
			"vod_content": ''
		}
		urlList = root.xpath("//div[@class='liveshow']/a")
		playUrl = ''
		for url in urlList:
			name = url.xpath("./text()")[0]
			purl = url.xpath("./@data-url")[0]
			playUrl =playUrl + '{0}${1}#'.format(name, purl)
		vod['vod_play_from'] = '体育直播'
		vod['vod_play_url'] = playUrl

		result = {
			'list': [
				vod
			]
		}
		return result

	def searchContent(self,key,quick):
		result = {}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		url = id
		if '04stream' in url:
			rsp = self.fetch(url)
			html = rsp.text
			strList = re.findall(r"eval\((.*?)\);", html)
			fuctList = strList[1].split('+')
			scrpit = ''
			for fuc in fuctList:
				if fuc.endswith(')'):
					append = fuc.split(')')[-1]
				else:
					append = ''
				Unicode = int(self.regStr(reg=r'l\((.*?)\)', src=fuc))
				char = chr(Unicode % 256)
				char = char + append
				scrpit = scrpit + char
			par = self.regStr(reg=r'/(.*)/', src=scrpit).replace(')', '')
			pars = par.split('/')
			infoList = strList[2].split('+')
			str = ''
			for info in infoList:
				if info.startswith('O'):
					Unicode = int(int(self.regStr(reg=r'O\((.*?)\)', src=info)) / int(pars[0]) / int(pars[1]))
					char = chr(Unicode % 256)
					str = str + char
			purl = self.regStr(reg=r"play_url=\'(.*?)\'", src=str)
			result["parse"] = 0
		elif 'v.stnye.cc' in url:
			purl = id
			result["parse"] = 1
		elif 'dplayer' in url:
			url = 'https://m.jrskbs.com' + url
			rsp = self.fetch(url)
			purl = self.regStr(reg=r'var PlayUrl = \"(.*?)\"', src=rsp.text)
			result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = purl
		result["header"] = ''
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
		return [200, "video/MP2T", action, ""]