#!/usr/bin/env python3


# from collections import namedtuple

from eliza import eliza
from main import response_message

eliza = eliza.Eliza()
eliza.load('doctor.txt')

# MessageEvent = namedtuple('MessageEvent', 'id text type')
class MessageEvent:
    def __init__(self, **entries):
        self.__dict__.update(entries)

if '__main__' == __name__:
    while True:
        said = input('> ')
        message = MessageEvent(**{'id':"000000000", 'text':said, 'type':"text"})
        response = response_message(message)
        if response is None:
            break
        print(response)

