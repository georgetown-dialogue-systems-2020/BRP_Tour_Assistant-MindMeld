# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain
in the MindMeld home assistant blueprint application
"""
from .root import app

@app.handle(intent='greet')
def greet(request, responder):
    try:
        responder.slots['name'] = request.context['name']
        prefix = 'Hi, {name}. '
    except KeyError:
        prefix = 'Hi. '
    responder.reply(prefix + 'I am your tour assistant. I can answer your questions about the Blue Ridge Pkwy.')
    responder.listen()
                    
@app.handle(intent='howru')
def howru(request, responder):
    responder.reply('I am good. What can I do for you today?')

@app.handle(intent='help')
def help(request, responder):
    responder.reply('You can ask me questions about restaurant, attractions, trials or anything you want to know about the Pkwy.')

@app.handle(intent='thanks')
def thanks(request, responder):
    responder.reply('You are welcome!')
    
@app.handle(intent='exit')
def exit(request, responder):
    responder.reply(['Bye!', 'Goodbye.', 'Have a nice day.', 'Peace out'])
