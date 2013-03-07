#!/usr/bin/python
# -*- coding: utf-8 -*- 

from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import uuid
from notify import notify

class Wish:
    def __init__(self, name, title, description):
        self.name = name
        self.title = title
        self.description = description

class Order:
    def __init__(self, username, remote_addr, wishlist, special, bequick):
        self.username = username
        self.remote_addr = remote_addr
        self.id = str(uuid.uuid4())
        self.wishlist = wishlist
        self.special = special
        self.bequick = bequick == "true"
        self.donothing = False
        
        if len(self.wishlist) is 0 and len(special) is 0: 
            self.wishstr = u"ничего не делать"
            self.donothing = True
        else:
            self.wishstr = ""
            i = 0
            for wish in wishlist:
                if i == 0:
                    pass
                elif i == len(wishlist) - 1:
                    self.wishstr += u" и "
                else:
                    self.wishstr += ", "
                self.wishstr += wish.title.lower()
                i += 1
            
            if len(special) > 0:
                if len(wishlist) > 0:
                    self.wishstr += " (" + special + ")"
                else:
                    self.wishstr = special
            
WISHBAR = []
NAME2WISH = {}
ORDERS = {}

def register(wish):
    WISHBAR.append(wish)
    NAME2WISH[wish.name] = wish

register(Wish("tea", u"Кружка чая", u"Черный или зеленый, с сахаром или без, с лимоном, а может быть ройбуш-ваниль? — уточняйте заказ в «особых пожеланиях»"))
register(Wish("coffee", u"Кружка кофе", u"С молоком, со взбитыми сливками, мороженым, сахаром, корицей или с виски :) — укажите в разделе «особых пожеланий»"))
register(Wish("drink", u"Прохладительный напиток", u"На выбор: сок (апельсин, яблоко, персик), CocaCola или морс"))
register(Wish("shampoo", u"Бокал шампанского", u"Ох уж эти пузырьки..."))
register(Wish("wine", u"Бокал вина", u"Италия, красное, a-la merlo"))
register(Wish("desert", u"Пироженка", u"Эклер, профитроли, ассорти... может быть, есть особые пожелания?"))
register(Wish("cake", u"Кусочек торта", u"Небольшой кусок торта Панчо из нежного бисквита, покрытого сочной глазурью или кусок фруктового торта"))
register(Wish("fruit", u"Фрукты", u"Бананы, яблоки, груши, виноград, мандарины..."))
register(Wish("strawberry", u"Клубника", u"Со взбитыми сливками, мороженым или просто так"))

@view_config(route_name="index_route")
def index(request):
    if request.method == "POST" and 'username' in request.cookies:
        username = request.cookies['username']
        # TODO process request
        wishlist = []
        for key,value in request.POST.items():
            if key.startswith("wish-"):
                wishlist.append(NAME2WISH[key[5:]])
                print("wish={}, value={}".format(key[5:], value))
        
        special = request.params["special"]
        bequick = request.params["bequick"]
        
        print(u"special={}, be quick={}".format(special,bequick))
        
        order = Order(username,request.remote_addr,wishlist,special,bequick)
        ORDERS[order.id] = order
        return HTTPFound(location = "/confirm/{}".format(order.id))
    else:
        if 'username' in request.cookies:
            username = request.cookies['username']
            response = render_to_response("pt/index.pt", { "username" : username, "wishbar" : WISHBAR }, request)
            response.set_cookie('username', value=username, max_age=86400)
            return response
        else:
            return render_to_response('pt/login.pt', {}, request)
        
@view_config(route_name="login_route")
def login(request):
    username = request.params['username']
    response = Response()
    response.set_cookie('username', value=username, max_age=86400)
    return HTTPFound(location = "/", headers=response.headers)        

@view_config(route_name="logout_route")
def logout(request):
    response = Response()
    response.set_cookie('username', value=None)
    return HTTPFound(location = "/", headers=response.headers)

@view_config(route_name="confirm_route")
def confirm(request):
    order_id = request.matchdict['order']
    if order_id in ORDERS.iterkeys():
        
        order = ORDERS.pop(order_id)
        
        # notify on new order
        notify(order)
        
        return render_to_response('pt/confirm.pt', { "order" : order }, request)
    else:
        return HTTPFound(location = "/")