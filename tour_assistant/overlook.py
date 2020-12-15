from .root import app
from .helper import _get_entity_milepost
from .helper import _handle_get_info


@app.handle(intent='ask_overlooks')
def answer_overlook(request, responder):
    responder.reply('There are almost 200 overlooks along the Blue Ridge Parkway.')
    responder.reply('Here is a list of the overlooks: https://www.virtualblueridge.com/parkway-places/overlooks/')
    responder.reply('You can also say \'recommend me some overlooks\', then I can recommend you some overlooks based on your preference of the milepost.')

@app.handle(intent='ask_overlook_intro')
def get_overlook_intro(request, responder):
    overlook_name, intro = _handle_get_info(request, info_name='intro')

    if intro:
        responder.reply(intro)
    else:
        responder.reply('Sorry, there is no introduction about this overlook.')

@app.handle(intent='ask_overlook_elevation')
def get_overlook_elevation(request,responder):
    overlook_name, elevation = _handle_get_info(request, info_name='elevation')

    if elevation:
        reply = 'The elevation of {name} is {elevation} feet.'.format(name=overlook_name, elevation=elevation)
        responder.reply(reply)
    else:
        responder.reply('Sorry, I don\'t know the elevation of this overlook.')

@app.handle(intent='ask_overlook_milepost')
def get_overlook_milepost(request,responder):
    overlook_name, milepost = _handle_get_info(request, info_name='milepost')
    
    if milepost:
        reply1 = 'The milepost of {name} is {milepost}.'.format(name=overlook_name, milepost=milepost)
        reply2 = '{name} is around milepost {milepost}.'.format(name=overlook_name, milepost=milepost)
        responder.reply([reply1, reply2])
    else:
        responder.reply('Sorry, I don\'t know the milepost of this overlook.')

@app.handle(intent='recommend_overlook')
def recommend_overlook(request,responder):
    milepost = _get_entity_milepost(request)

    responder.frame['activity'] = 'ASK_OVERLOOK'

    if milepost:
        _handle_recommend_overlook(responder, milepost)
    else:
        responder.reply('Please specify the milepost.')

@app.handle(intent='specify_overlook_info')
def specify_overlook_info(request, responder):
    milepost = _get_entity_milepost(request)

    if responder.frame['activity'] == 'ASK_OVERLOOK' and milepost:
        _handle_recommend_overlook(responder, milepost)
    elif not responder.frame['activity']:
        responder.reply('Sorry, I don\'t know what do you mean.')

# helper

# if there is an interactive 360-degree view available, send the link to users
def _prompt_360_degree_view(overlook_name):
    # kb: knowledge base
    kb = app.question_answerer.get(index=overlooks, name=overlook_name)

    if kb[0]['link']:
        reply = 'You can ckeck the interactive 360-degree view here: {link}'.format(link=kb[0]['link'])
        responder.reply(reply)

def _handle_recommend_overlook(responder, milepost):
    idx = 'overlooks'
    entity_name = 'overlooks'

    # kb: knowledge base
    kb = app.question_answerer.get(index=idx, size=200)

    # set the range of the milepost
    milepost_min = milepost - 2 if milepost >= 2 else 0
    milepost_max = milepost + 2 if milepost <=467 else 469

    cnt = 0
    nearest_entity = kb[0]['name']  # name of the nearest overlook
    nearest_milepost = kb[0]['milepost']
    for entity in kb:
        # find the overlooks meet the condition(milepost)
        if milepost_min <= entity['milepost'] <= milepost_max:
            cnt += 1
            if cnt == 1:
                reply_1 = 'Here are some {entity} from milepost {min} to {max}: '.format(entity=entity_name, min=milepost_min, max=milepost_max)
                responder.reply(reply_1)
            reply_2 = '    MILEPOST: {milepost} NAME: {name}'.format(milepost=entity['milepost'], name=entity['name'])
            responder.reply(reply_2)

        # in case no overlooks is found, memorize(update) the nearest overlook
        if abs(milepost - entity['milepost']) < abs(milepost - nearest_milepost):
            # update the nearest overlook name and the milepost
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

