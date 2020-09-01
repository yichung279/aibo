import logging
import os
import re
import sys
from datetime import datetime
from os.path import join

from chat.chatbot import config as chat_config
from chat.chatbot.answerer import answerer

# from chat.chatbot.chatter.chatter import Chatter


def logging_setting():
    if chat_config.debug:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


def get_question_key(text):
    '''
    Description:
            Try to get question keyword from text(rule-based).

    '''
    explain = ['知道', '理解', '解釋', '了解', '瞭解', '告訴我', '跟我說', '懂', '懂不懂']
    base_q = ['什麼', '甚麼', '誰', '啥', '的意思']
    q_end = ['?', '阿', '啊', '嗎', '呢', '？']

    text = text.replace('是', '')
    for _end in q_end:
        text = text.replace(_end, '')

    # print(text)
    explain_pattern = '|'.join(explain)
    base_q_pattern = '|'.join(base_q)

    patterns = [
        (f'.*({explain_pattern})({base_q_pattern})(.+)', 3),
        (f'.*({explain_pattern})(.+)({base_q_pattern})', 2),
        (f'.*({base_q_pattern})(.+)', 2),
        (f'(.+)({base_q_pattern})', 1),
        (f'.*({explain_pattern})(.+)', 2),
    ]

    for pattern in patterns:
        m = re.match(pattern[0], text)
        if m and m.group(pattern[1]) != '':
            return m.group(pattern[1])

    return None


class ChatBot():
    def __init__(self):
        # self.chatter_bot = Chatter(chat_config.chatter)
        self.chatlog_writer = self._get_chatlog_writer()

    def __del__(self):
        self._write_chatlog("------對話結束------\n")
        self._write_chatlog("\n")

        if self.chatlog_writer:
            self.chatlog_writer.close()

    def _get_chatlog_writer(self):
        if not chat_config.chatlog_path:
            return None
        else:
            chatlog_writer = open(chat_config.chatlog_path,
                                  'a+', encoding='utf-8')
            chatlog_writer.write("---聊天開始於 {} :---\n".format(datetime.now()))
            return chatlog_writer

    def _write_chatlog(self, text):
        if self.chatlog_writer:
            self.chatlog_writer.write(text + '\n')

    def response(self, text):
        self._write_chatlog('user: ' + text)

        # 獲取問題關鍵字
        question_key = get_question_key(text)
        # print(f'question_key: {question_key}')
        response = None

        # 若有得到問題的關鍵字則丟去answerer回答
        if question_key is not None:
            response = answerer.response(question_key)

        # if response:
        #     logging.info('answerer: ' + response)
        # else:
        #     # 若是沒有得到問題關鍵字或是answerer回答不出來，則丟去chatter聊天
        #     response = self.chatter_bot.response(text)
        #     logging.info('chatter: ' + response)

        # 預防空字串
        if not response:
            logging.info('response is empty!!!!')
            response = '我不清楚你在說啥ㄟ'

        self._write_chatlog('chatbot: ' + response)
        return response


def chat(text):
    logging_setting()
    chatbot = ChatBot()
    response = chatbot.response(text)
    return response


def test():
    logging_setting()
    chatbot = ChatBot()
    while True:
        try:
            text = input("user:")
            response = chatbot.response(text)
            print('chatbot:', response)

        except KeyboardInterrupt:
            break
    return


if __name__ == "__main__":
    test()
