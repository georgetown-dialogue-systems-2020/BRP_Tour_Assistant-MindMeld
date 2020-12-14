from .root import app
from .helper import _handle_get_info

CUR_TRAIL_NAME = None

# when users ask for a trail's length
@app.handle(intent='ask_trail_length')
def send_trail_length(request, responder):
    trail_name, length = _handle_get_info(request, 'length')

    reply = 'The length of {name} is {length} miles'.format(name=trail_name, length=length)
    responder.reply(reply)
    
# when users ask for a trail's milepost
@app.handle(intent='ask_trail_milepost')
def send_trail_milepost(request, responder):
    trail_name, milepost = _handle_get_info(request, 'milepost')

    reply = '{name} is around milepost {milepost}'.format(name=trail_name, milepost=milepost)
    responder.reply(reply)

# when users ask for a trail's skill level
@app.handle(intent='ask_trail_skill_level')
def send_trail_skill_level(request, responder):
    trail_name, skill_level = _handle_get_info(request, 'skill_level')

    reply = 'The skill level of {name} is {skill_level}'.format(name=trail_name, skill_level=skill_level)
    responder.reply(reply)

# Instead of providing the whole trails list,
# it looks better to show users the website of trails information
@app.handle(intent='ask_trails')
def show_all_trails(request, responder):
    responder.reply('There are over 100 trails of all skill levels along the Parkway in North Carolina and Virginia.')
    responder.reply('You can easily find all the trails information on the website: https://www.blueridgeparkway.org/hiking/')
    responder.reply('Or say \'recommend me some trails\', I can show you some trails based on your preference of skill level and length')

    # responder.listen()

# randomly recommend a trail to users
# recommend trails based on users' choices of skill level and length
# 1. expected skill level + length smaller than or equal expected length
# 2. otherwise, expected skill level
@app.handle(intent='recommend_trail')
def recommend_trail(request, responder):
    skill_level = _get_trail_skill_level(request)
    length = _get_trail_length(request)

    responder.frame['activity'] = 'ASK_TRAIL'

    if skill_level and length:
        _handle_recommend_trail(responder, skill_level, length)
    elif skill_level:
        responder.frame['skill_level'] = skill_level
        responder.frame['length'] = None
        responder.reply('Ok, how about the length (miles)?')
        # responder.listen()
    elif length:
        responder.frame['skill_level'] = None
        responder.frame['length'] = length
        responder.reply('Ok, how about the skill_level?')
        # responder.listen()
    else:
        responder.frame['skill_level'] = None
        responder.frame['length'] = None
        responder.reply('Ok, how about the skill_level?')

@app.handle(intent='specify_trail_info')
def specify_trail_info(request, responder):
    skill_level = _get_trail_skill_level(request)
    length = _get_trail_length(request)

    if skill_level and length:
        _handle_recommend_trail(responder, request.frame['skill_level'], request.frame['length'])
    elif request.frame['skill_level'] and length:
        _handle_recommend_trail(responder, request.frame['skill_level'], length)
    elif request.frame['length'] and skill_level:
        _handle_recommend_trail(responder, request.frame['length'], skill_level)
    elif skill_level and not length:
        responder.frame['skill_level'] = skill_level
        responder.reply('Ok, how about the length?')
    elif length and not skill_level:
        responder.frame['length'] = length
        responder.reply('Ok, how about the skill level?')
    else:
        responder.reply('Please specify the skill level and length (miles) of the trails you prefer. You can also say any skill level and any length.')


# helper

def _get_trail_skill_level(request):
    trail_skill_level = next((e for e in request.entities if e['type'] == 'skill_level'), None)

    return trail_skill_level['text'] if trail_skill_level else None

def _get_trail_length(request):
    trail_length = next((e for e in request.entities if e['type'] == 'sys_number'), None)

    return trail_length['value'][0]['value'] if trail_length else None

def _handle_recommend_trail(responder, skill_level, length):
    trails = app.question_answerer.get(index='trails', skill_level=skill_level, size=150)

    cnt = 0
    for trail in trails:
        if trail['length'] <= length:
            cnt += 1
            reply = '{name}    {skill_level}    {length} miles'.format(name=trail['trail_name'], skill_level=skill_level, length=trail['length'])
            responder.reply(reply)

    if cnt == 0:
        responder.reply("Sorry, it seems that no trails meet your requirments.")
        reply = 'Here are five {skill_level} trails I recommend to you.'.format(skill_level=skill_level)
        responder.reply(reply)

        cnt = 0
        for trail in trails:
            cnt += 1
            reply = '{name}    {skill_level}    {length} miles'.format(name=trail['trail_name'], skill_level=skill_level, length=trail['length'])
            responder.reply(reply)
