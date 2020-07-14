#!/usr/bin/env python3


#
import json

# third-party imports
import uvicorn
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from pydantic import BaseModel

# local imports
import config

app = FastAPI()
line_bot_api = LineBotApi(config.access_token) # Channel Access Token
handler = WebhookHandler(config.secret) # Channel Secret

class Item(BaseModel):
    events: list
    destination: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/callback/')
async def callback(item: Item, request: Request):
    signature = request.headers['X-Line-Signature'] # get X-Line-Signature header value
    # keep string format as returned string of flask.requset.get_data()
    body = json.dumps(dict(item), ensure_ascii=False, separators=(',', ':'))
    # app.logger.info("Request body: " + body) # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print(e)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '機器人你好':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hi I\'m SinoPac AI bot')
        )
    if 'group' == event.source.type:
        user_id = event.source.group_id
    elif 'room' == event.source.type:
        user_id = event.source.room_id
    else:
        user_id = event.source.user_id

    conn = sqlite3.connect('crawler.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO user (userid) VALUES(\'%s\')" %user_id)
    conn.commit()
    print('user saved')


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.host, port=config.port, ssl_keyfile=config.key, ssl_certfile=config.cert)
