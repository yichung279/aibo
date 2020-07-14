#!/usr/bin/env python3


# standard import
import json

# third-party import
import uvicorn
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from model.Model import ShareLog, User
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# local import
import config
from eliza import eliza


app = FastAPI()
line_bot_api = LineBotApi(config.access_token) # Channel Access Token
handler = WebhookHandler(config.secret) # Channel Secret

eliza = eliza.Eliza()
eliza.load('doctor.txt')

class event_item(BaseModel):
    events: list
    destination: str

class share_item(BaseModel):
    poster: str
    url: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/share")
async def share(item: share_item):
    poster = item.poster
    url = item.url
    share_time = datetime.now().strftime('%Y%m%d_%H:%M:%S')
    html_name = share_time.strftime('%Y%m%d_%H:%M:%S') + 'html'

    with open(f'./html/{html_name}', 'w')as f:
        f.write(requests.get(url).text)

    engine = create_engine(config.db_url)
    Session = sessionmaker(bind=engine)()
    Session.execute(ShareLog.insert(prefixes=['OR IGNORE']),
                    {"poster": poster, "url": url, "html_name": html_name, "share_time": share_time})
    Session.commit()
    Session.close()

    return {"message": "Shared"}

@app.post('/callback/')
async def callback(item: event_item, request: Request):
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
            TextSendMessage(text=eliza.initial())
        )
    else:
        said = event.message.text
        response = eliza.respond(said)
        if response is None:
            response = 'りしれ供さ小?'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

    if 'group' == event.source.type:
        user_id = event.source.group_id
    elif 'room' == event.source.type:
        user_id = event.source.room_id
    else:
        user_id = event.source.user_id

    # sqlalchemy orm
    engine = create_engine(config.db_url)
    Session = sessionmaker(bind=engine)()
    Session.execute(User.insert(prefixes=['OR IGNORE']), {"user_id": user_id})
    Session.commit()
    Session.close()
    print('user saved')


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.host, port=config.port, ssl_keyfile=config.key, ssl_certfile=config.cert)
