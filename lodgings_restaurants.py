from .root import app
from .helper import _get_entity_milepost
from .helper import _handle_get_info


@app.handle(intent='ask_lodgings')
@app.handle(intent='ask_food')
def answer_food_lodging(request, responder):
    if request.intent == 'ask_lodging':
        responder.reply('There are lots of hotels, motels along the parkway.')
        responder.reply('You can say \'recommend me some hotels around milepost 123.4, I can provide you some hotels based on your preference of the milepost.\'')
    else:
        responder.reply('There are lots of restaurants along the parkway.')
        responder.reply('You can say \'recommend me some restaurants around milepost 123.4, I can provide you some restaurants based on your preference of the milepost.\'')


# when users ask for the information about a specific hotel or restaurant
# get a brief introduction
@app.handle(intent='ask_lodging_intro')
@app.handle(intent='ask_restaurant_intro')
def send_intro(request, responder):
    _, intro = _handle_get_info(request, info_name='intro')

    responder.reply(intro)

# get the address of a specific hotel or restaurant
@app.handle(intent='ask_lodging_address')
@app.handle(intent='ask_restaurant_address')
def send_address(request, responder):
    entity_name, address = _handle_get_info(request, info_name='address')

    reply = 'The address of {name} is {address}.'.format(name=entity_name, address=address)
    responder.reply(reply)
	
@app.handle(intent='ask_lodging_milepost')
@app.handle(intent='ask_restaurant_milepost')
def send_milepost(request, responder):
    entity_name, milepost = _handle_get_info(request, info_name='milepost')

    reply = '{name} is around milepost {milepost}.'.format(name=entity_name, milepost=milepost)
    responder.reply(reply)

@app.handle(intent='ask_lodging_tel')
@app.handle(intent='ask_restaurant_tel')
def send_tel(request, responder):
    _, tel = _handle_get_info(request, info_name='tel')

    reply = 'Here is the telephone number: {tel}.'.format(tel=tel)
    responder.reply(reply)

@app.handle(intent='ask_lodging_website')
@app.handle(intent='ask_restaurant_website')
def send_website(request, responder):
    _, website = _handle_get_info(request, info_name='website')

    reply = 'Here is the website: {web}.'.format(web=website)
    responder.reply(reply)

@app.handle(intent='recommend_lodging')
@app.handle(intent='recommend_restaurant')
def recommend_lodging_restaurant(request, responder):
    milepost = _get_entity_milepost(request)

    responder.frame['activity'] = 'ASK_LODGING' if request.intent == 'recommend_lodging' else 'ASK_RESTAURANT'

    if milepost:
        _handle_recommend_lodging_restaurant(responder, milepost)
    else:
        responder.reply('Please specify the milepost.')

@app.handle(intent='specify_lodging_info')
@app.handle(intent='specify_restaurant_info')
def specify_info(request, responder):
    milepost = _get_entity_milepost(request)

    if (responder.frame['activity'] == 'ASK_LODGING' or responder.frame['activity'] == 'ASK_RESTAURANT') and milepost:
        _handle_recommend_lodging_restaurant(responder, milepost)
    elif not responder.frame['activity']:
        responder.reply('Sorry, I don\'t know what do you mean.')


# helper

def _handle_recommend_lodging_restaurant(responder, milepost):
    if responder.frame['activity'] == 'ASK_LODGING':
        idx = 'lodgings'
        entity_name = 'hotels'
    elif responder.frame['activity'] == 'ASK_RESTAURANT':
        idx = 'restaurants'
        entity_name = 'restaurants'

    # kb: knowledge base
    kb = app.question_answerer.get(index=idx, size=50)

    # set the range of the milepost
    milepost_min = milepost - 5 if milepost >= 5 else 0
    milepost_max = milepost + 5 if milepost <=464 else 469

    cnt = 0
    nearest_entity = kb[0]['name']  # name of the nearest hotel or restaurant
    nearest_milepost = kb[0]['milepost']
    for entity in kb:
        # find the lodgings/restaurants meet the condition(milepost)
        if milepost_min <= entity['milepost'] <= milepost_max:
            cnt += 1
            if cnt == 1:
                reply_1 = 'Here are some {entity} from milepost {min} to {max}: '.format(entity=entity_name, min=milepost_min, max=milepost_max)
                responder.reply(reply_1)
            reply_2 = '    MILEPOST: {milepost} NAME: {name}'.format(milepost=entity['milepost'], name=entity['name'])
            responder.reply(reply_2)

        # in case no lodging/restaurant is found, memorize(update) the nearest lodging/restaurant
        if abs(milepost - entity['milepost']) < abs(milepost - nearest_milepost):
            # update the nearest lodging/restaurant name and the milepost
            nearest_entity = entity['name']
            nearest_milepost = entity['milepost']

    if cnt == 0:
        reply_3 = 'Sorry, I don\'t find any {entity} around milepost {milepost}.'.format(entity=entity_name, milepost=milepost)
        responder.reply(reply_3)
        reply_3 = 'Here is the nearest {entity} to the milepost {milepost}:'.format(entity=entity_name, milepost=milepost)
        responder.reply(reply_3)
        reply_3 = '    MILEPOST: {milepost} NAME: {name}'.format(milepost=nearest_milepost, name=nearest_entity)
        responder.reply(reply_3)

    # prompt
    reply_4 = 'I can tell you more information about the {entity}. Like the address, telephone number, and their websites.'.format(entity=entity_name)
    responder.reply(reply_4)
