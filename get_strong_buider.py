import requests
import json
import datetime


d = 0
url = "http://206.189.145.39:1337/devotions?strdate={}"
curr_date = '{0:%Y-%m-%d}'.format(datetime.date.today()+ datetime.timedelta(days=d))
header = {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }

a = requests.get(url.format(curr_date),headers=header)
#b = json.loads(a.text)[0]

while(a.text != '[]' ):

	b = json.loads(a.text)[0]
	b['m2'] = b['m2'].replace('<p>','\n').replace('</p>','\n').replace('&ldquo;','\"').replace('&rdquo;','\"').replace('&rsquo;','\'').replace('&emsp;','').replace('&lsquo;','\'').replace('<br />','\n')
	b['verse'] = b['verse'].replace('<br />','\n').replace('</p>','\n').replace('<p><span style=\"text-decoration: underline;\"><strong>','\n').replace('</strong></span>','')
	json_format = {
		'title':b['title'],
		'bacaan':b['m1'],
		'isi':b['m2'],
		'pertanyaan':b['m3'],
		'bagikan':b['m4'],
		'verses':b['verse'],
		'date': b['strdate']
	}

	with open('sb/'+curr_date+'.json', "w") as write_file:
		json.dump(json_format, write_file)
	d += 1
	print("[+] "+curr_date)
	curr_date = '{0:%Y-%m-%d}'.format(datetime.date.today()+ datetime.timedelta(days=d))
	a = requests.get(url.format(curr_date),headers=header)