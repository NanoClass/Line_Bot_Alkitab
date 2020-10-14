import requests
from bs4 import BeautifulSoup
import json

def get_renungan():
	src = "http://alkitab.mobi/renungan/sh/"
	a = requests.get(src)
	b = BeautifulSoup(a.text,'html.parser')
	c = b.find_all('div')[3].find_all('p')
	title = c[1].text
	bacaan = c[0].text
	isi = c[2].text
	i = 3
	while not c[i].text.startswith("Doa: "):
		isi +='\n\n'+c[i].text
		i+=1
	doa = c[i].text
	
	return title,bacaan,isi,doa