#!/usr/bin/env python3


# standard import
import json
import os
import re
from datetime import datetime

# third-party import
import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from model.Model import User, CollectLog
from pydantic import BaseModel
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional

# local import
import config
from eliza import eliza


app = FastAPI()
app.mount("/static", StaticFiles(directory="web/dist"), name="static")

line_bot_api = LineBotApi(config.access_token) # Channel Access Token
handler = WebhookHandler(config.secret) # Channel Secret

engine = create_engine(config.db_url)
eliza = eliza.Eliza()
eliza.load('doctor.txt')

templates = Jinja2Templates(directory="web/dist")


class WebhookEventObject(BaseModel):
    events: list
    destination: str

class News(BaseModel):
    poster: str
    urls: List[str]

class Oracle(BaseModel):
    message: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ui/{api_name}")
async def get_ui(request: Request, api_name: str):
    if 'oracle' == api_name:
        return templates.TemplateResponse("oracle.html", {'request': request})
    elif 'news' == api_name:
        return templates.TemplateResponse("news.html", {'request': request})
    elif 'checkedNews' == api_name:
        return templates.TemplateResponse("checkedNews.html", {'request': request})
    else:
        return {"message": "no this ui"}

@app.post("/oracle/")
async def broadcast(oracle: Oracle):
    Session = sessionmaker(bind=engine)()
    for instance in Session.query(User).all():
        try:
            line_bot_api.push_message(instance.user_id, TextSendMessage(text=oracle.message))
        except LineBotApiError as e:
            raise e
    return {"message": "broadcasted"}

@app.post("/checkedNews/")
async def publish(urls: List[str]):
    Session = sessionmaker(bind=engine)()
    success_publish = []
    for instance in Session.query(User).all():
        for url in urls:
            try:
                line_bot_api.push_message(instance.user_id, TextSendMessage(text=url))
                success_publish.append(url)
            except LineBotApiError as e:
                raise e
    published_time = datetime.now()
    try:
        update_collect_log(Session, success_publish, published_time)
        print('message published')
    except Exception as e:
        print(e)
    return {"message": "published"}

@app.get("/news/{num_news}")
def get_latest_num_news(num_news: int):
    Session = sessionmaker(bind=engine)()
    q = Session.query(CollectLog).order_by(CollectLog.collect_time).limit(num_news)
    latest_N_news = []
    for instance in q:
        instance = instance.__dict__
        instance.pop('html', None)
        latest_N_news.append(instance)
    return latest_N_news

@app.post("/news/")
async def collect(news: News):
    objects = []
    try:
        for url in news.urls:
            html = requests.get(url).text
            collect_time = datetime.now()
            objects.append(CollectLog(poster=news.poster, url=url, html=html, collect_time=collect_time))
        collect_news_to_db(objects)
        print(f'{news.urls} collected')
    except Exception as e:
        print(e)
    return {"message": "collected"}

@app.post('/callback/')
async def callback(item: WebhookEventObject, request: Request):
    signature = request.headers['X-Line-Signature'] # get X-Line-Signature header value
    # keep string format as returned string of flask.requset.get_data()
    body = json.dumps(dict(item), ensure_ascii=False, separators=(',', ':'))
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print(e)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    save_user_id(event.source)
    response = response_message(event.message)
    if response:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))

def collect_news_to_db(objects: List[object]):
    Session = sessionmaker(bind=engine)()
    CollectLog.metadata.create_all(engine)
    Session.bulk_save_objects(objects)
    Session.commit()
    Session.close()

def save_user_id(source):
    if 'group' == source.type:
        user_id = source.group_id
    elif 'room' == source.type:
        user_id = source.room_id
    else:
        user_id = source.user_id

    # sqlalchemy orm
    Session = sessionmaker(bind=engine)()

    User.metadata.create_all(engine)
    user_table = Table(User.__tablename__, MetaData(), autoload_with=engine)

    Session.execute(user_table.insert(prefixes=['OR IGNORE']), {"user_id": user_id})
    Session.commit()
    Session.close()

    print('user saved')

def response_message(message):
    response = None
    text =  message.text.lower()
    if text == '機器人你好':
        response = eliza.initial()

    elif re.findall(r'aibo', text):
        said = text.replace('aibo', '')
        response = eliza.respond(said)
        if response is None:
            response = '開發中'

    return response

def update_collect_log(Session: object, success_publish: List[str], published_time: datetime):
    Session.query(CollectLog)\
        .filter(CollectLog.url.in_(success_publish))\
        .update({\
                 CollectLog.published: True,\
                 CollectLog.published_time: published_time}, synchronize_session=False)
    Session.commit()
    Session.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.host, port=config.port, ssl_keyfile=config.key, ssl_certfile=config.cert, reload=True)
