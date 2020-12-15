# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'unknown' domain in
the home assistant blueprint application
"""
from .root import app


@app.handle(intent='unknown')
def unknown(request, responder):
    responder.reply("Sorry, not sure what you meant there.")
    responder.reply("You can ask:")
    responder.reply("1. Show me the trials information")
    responder.reply("2. What's the length of the mountain farm trial?")
    responder.reply("3. Where can I find a restaurant?")
    responder.reply("4. Where can I find a restaurant around milepost 86?")
    responder.reply("5. Where can I find a hotel?")
    responder.reply("6. Where can I find a hotel around milepost 365?")
    responder.reply(". . . . . .")
