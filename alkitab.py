import requests
from bs4 import BeautifulSoup
import re


def alkitab_req(kitab='kejadian', pasal='1', ayat='1',ver='tb'):
	src = 'http://alkitab.mobi/{}/{}/{}/{}/'
	return alkitab_url(src.format(ver,kitab,pasal,ayat))

def alkitab_url(url):
	try: 
		header = {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
		a = requests.get(url,headers = header)
		b = BeautifulSoup(a.text,'html.parser')
		e = {}
		e['title'] = b.find('title').text
		e['ayat'] = b.find('p').text[4:]
		e['next'] = b.find('a',{'accesskey':'9'})['href']
		e['prev']= b.find('a',{'accesskey':'7'})['href']
		return e
	except:
		return '[-] ERROR IN ALKITAB_URL'

def alkitab_view(kitab='kejadian', pasal='1', ayat='1',ver='tb'):
	curr_view = alkitab_req(kitab,pasal,ayat,ver)
	json_verse_template = {
	  "type": "bubble",
	  "body": {
	    "type": "box",
	    "layout": "vertical",
	    "contents": [
	      {
	        "type": "text",
	        "text": curr_view['title'],
	        "weight": "bold",
	        "size": "md"
	      },
	      {
	        "type": "text",
	        "margin": "md",
	        "text" : curr_view['ayat'],
	        "wrap" : True
	      }]},
	      "footer":{
	        "type" : "box",
	        "layout" : "horizontal",
	        "spacing" : "md",
	        "contents":[
	          {
	            "type" : "button",
	            "color": "#202421",
	            "style": "primary",
	            "action": {
	              "type": "postback",
	              "label": "BACK",
	              "data":"al="+curr_view['prev']
	            }
	          },
	          {
	            "type" : "button",
	            "style": "primary",
	            "action": {
	              "type": "postback",
	              "label": "NEXT",
	              "data":"al="+curr_view['next']
	            }
	          }]
	      }
	}
	return json_verse_template

def alkitab_view2(a):
	curr_view = alkitab_url(a)
	json_verse_template = {
	  "type": "bubble",
	  "body": {
	    "type": "box",
	    "layout": "vertical",
	    "contents": [
	      {
	        "type": "text",
	        "text": curr_view['title'],
	        "weight": "bold",
	        "size": "md"
	      },
	      {
	        "type": "text",
	        "margin": "md",
	        "text" : curr_view['ayat'],
	        "wrap" : True
	      }]},
	      "footer":{
	        "type" : "box",
	        "layout" : "horizontal",
	        "spacing" : "md",
	        "contents":[
	          {
	            "type" : "button",
	            "color": "#202421",
	            "style": "primary",
	            "action": {
	              "type": "postback",
	              "label": "BACK",
	              "data":"al="+curr_view['prev']
	            }
	          },
	          {
	            "type" : "button",
	            "style": "primary",
	            "action": {
	              "type": "postback",
	              "label": "NEXT",
	              "data":"al="+curr_view['next']
	            }
	          }]
	      }
	}
	return json_verse_template

def parse_alkitab(a):
	msg_temp = re.findall('[0-9][A-Za-z-]+|[0-9] [A-Za-z-]+|[A-Za-z]+|[0-9]+',a)
	msg_temp[0] = msg_temp[0].replace(' ','')
	b =""
	print(msg_temp)
	try:
		try:
			if msg_temp[3].lower() == 'kjv':
				msg_temp[3] = 'av'
		except:
			pass

		if len(msg_temp) == 1:
			b = alkitab_view(msg_temp[0])
		elif len(msg_temp) == 2:
			b = alkitab_view(msg_temp[0],msg_temp[1])
		elif len(msg_temp) == 3:
			b = alkitab_view(msg_temp[0],msg_temp[1],msg_temp[2])
		elif len(msg_temp) == 4:
			b = alkitab_view(msg_temp[0],msg_temp[1],msg_temp[2],msg_temp[3])
		return b
	except:
		return '[-] ERROR IN PARSE ALKITAB'