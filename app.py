from flask import Flask, request, abort, send_from_directory
from bs4 import BeautifulSoup
import requests
import re
import datetime

#dari github line bot sdk
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent, PostbackAction
)

#import Custom Library
try:
	from alkitab import *
	from ayat_scrap import *
	from strong_builder import *
	from renungan import *
	from help import *
except:
	print('[+] Error Import Custom Library')



ACCESS_TOKEN = << ACCESS TOKEN >>
WEBHOOK = << WEBHOOK TOKEN >>

LineApi = 'https://api.line.me/v2/bot/message/reply'
req_header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ACCESS_TOKEN}

bot = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(WEBHOOK)


app = Flask(__name__, static_url_path='/assets')
application = app # our hosting requires application in passenger_wsgi

@app.route("/assets")
def assets():
	return "Forbidden"

@app.route("/assets/js/<path:path>")
def send_js(path):
	return send_from_directory('assets/js', path)

@app.route("/assets/image/<path:path>")
def send_image(path):
	return send_from_directory('assets/image', path)

@app.route("/") #path to web
def index():
	return "Active"
	
@app.route("/callback", methods=['POST']) #callback
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    
@handler.add(MessageEvent,message=TextMessage)
def handle_text_message(event):

	userid_line = event.source.user_id
	profile = bot.get_profile( userid_line )
	
	msg = event.message.text
	msg = msg.lower()

	# Jika Program berhasil Dijalankan
	if "/test" == msg:
		bot.reply_message(event.reply_token,TextSendMessage("Success"))
	elif "/ah" == msg:
		bot.reply_message(event.reply_token,TextSendMessage(text = ayat_json()))
	elif msg.startswith("/al"):
		tmp = msg[3:]
		requests.post(LineApi ,headers = req_header,data= json.dumps({'replyToken':event.reply_token, 'messages': [{"type": "flex", "altText": "ayat", "contents":parse_alkitab(tmp)}]}))
	elif "/sb" == msg:
		curr_date = '{0:%d-%m-%Y}'.format(datetime.date.today())
		title,m1,m2,m3,m4 = get_sb()
		title = 'Tanggal : '+curr_date+'\n'+title +'\n> '+m1+' <'
		m2 = 'Merenungkan :'+m2
		m3 = 'Melakukan :\n'+m3
		m4 = 'Membagikan :\n'+m4
		requests.post(LineApi ,headers = req_header,data= json.dumps({'replyToken':event.reply_token, 'messages': [{"type":"text","text":title},{"type":"text","text":m2},{"type":"text","text":m3},{"type":"text","text":m4}]}))
	elif "/rh" == msg:
		title,bacaan,isi,doa = get_renungan()
		requests.post(LineApi ,headers = req_header,data= json.dumps({'replyToken':event.reply_token, 'messages': [{"type":"text","text":title},{"type":"text","text":bacaan},{"type":"text","text":isi},{"type":"text","text":doa}]}))
	elif "/sb-ay" == msg:
		bot.reply_message(event.reply_token,TextSendMessage(text = get_ayat_sb()[1:]))
	elif "/help" == msg:
		requests.post(LineApi ,headers = req_header,data= json.dumps({'replyToken':event.reply_token, 'messages': [{"type": "flex", "altText": "help", "contents":about()}]}))


@handler.add(PostbackEvent)
def postback(event):
	data = event.postback.data
	if data.startswith("al"):
		requests.post(LineApi ,headers = req_header,data= json.dumps({'replyToken':event.reply_token, 'messages': [{"type": "flex", "altText": "ayat", "contents":alkitab_view2(data[3:])}]}))



if __name__ == "__main__":
    app.run()