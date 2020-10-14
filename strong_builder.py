#python 3.7
import requests
import json
import datetime

def get_sb():
	curr_date = '{0:%Y-%m-%d}'.format(datetime.date.today())
	with open('sb/'+curr_date+'.json', 'r') as f:
		b = datastore = json.load(f)
	return b['title'],b['bacaan'],b['isi'],b['pertanyaan'],b['bagikan']

def get_ayat_sb():
	curr_date = '{0:%Y-%m-%d}'.format(datetime.date.today())
	with open('sb/'+curr_date+'.json', 'r') as f:
		b = datastore = json.load(f)
	return b['verses']