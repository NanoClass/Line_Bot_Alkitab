# python 3
from bs4 import BeautifulSoup
import requests
import re

def get_ayat():
	src = 'https://www.alkitabku.com/'
	a = requests.post(src)
	b = BeautifulSoup(a.text,'html.parser')
	c = b.find(class_='blockquote-color-bg-dark')
	e = c.find('p').getText()
	f = c.find('footer').getText()
	g = "Fitur ini Sedang Dalam Perbaikan"
	return g

def ayat_json(lang='tb'):
	header = {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
	src = 'https://www.verseoftheday.com/'
	a = requests.post(src,headers=header)
	b = BeautifulSoup(a.text,'html.parser')
	c = b.find_all('a')[1].getText()
	e = re.split(':| ',c)
	src_al = 'http://alkitab.mobi/{}/{}/{}/{}/'.format(lang,e[0],e[1],e[2])
	print(src_al) 
	f = requests.get(src_al,headers = header)
	g = BeautifulSoup(f.text,'html.parser')
	i={}
	i['title'] = g.find('title').text
	i['ayat'] = g.find('p').text[4:]
	return i['ayat']+'\n- '+i['title']
	