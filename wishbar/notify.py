#!/usr/bin/python
# -*- coding: utf-8 -*- 

import xmpp 
import Queue
import time

USERNAME = 'username' # @gmail.com
PASSWORD = 'password'

class User():
    def __init__(self,uri,name):
        self.uri = uri
        self.name= name

USERS = {
    "user@gmail.com" : User("user@gmail.com",u"Имя пользователя")
}

def notify(order):
    cnx = xmpp.Client('gmail.com')
    cnx.connect( server=('talk.google.com',5223) )

    cnx.auth(USERNAME,PASSWORD,'botty')
   
    message = order.username + " (" + order.remote_addr + "): "
    if order.donothing:
        message += u"ничего не делать"
    else:
        message += order.wishstr
    if order.bequick:
        message += u", быстро-быстро"
    for user in USERS.itervalues():
        cnx.send(xmpp.Message(user.uri, message, typ='chat'))

QUEUE = Queue.Queue()

def confirm(cnx, hero, message):
    for user in USERS.itervalues():
        QUEUE.put(xmpp.Message(user.uri, u"Вызвался {} ({}): {}".format(hero.name, hero.uri, message), typ='chat'))
    
def message_callback(cnx, message):
    t = message.getType()
    if t in ['message', 'chat', None]:
        if message.getBody():
            uri = message.getFrom().getStripped()
            if uri in USERS.iterkeys():
                print(u"{}: {}".format(message.getFrom().getStripped(), message.getBody()))
                confirm(cnx, USERS[uri], message.getBody())
    else:
        print(u"message type=={}".format(t))
        time.sleep(10)

def run_bot():
    cnx = xmpp.Client('gmail.com')
    cnx.connect( server=('talk.google.com',5223) )

    cnx.auth(USERNAME,PASSWORD,'botty')
    cnx.RegisterHandler('message', message_callback)
    cnx.sendInitPresence()
    
    while True:
        if not QUEUE.empty():
            msg = QUEUE.get()
            cnx.send(msg)
            QUEUE.task_done()
        
        time.sleep(5) # little timeout to prevent blocking
        cnx.Process(1)
        
    print("finished")
