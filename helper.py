# Here are some useful helpers used for multiple domains
# Some other help functions are included in different python files for different domains
from .root import app

def _get_entity_name(request, entity_label):
    entity_name = next((e for e in request.entities if e['type'] == entity_label), None)

    return entity_name['text'] if entity_name else None

def _get_entity_milepost(request):
    entity_milepost = next((e for e in request.entities if e['type'] == 'sys_number'), None)

    return entity_milepost['value'][0]['value'] if entity_milepost else None

def _handle_get_info(request, info_name):
    if request.domain == 'lodgings':
        idx = 'lodgings'
        entity_label = 'lodging'
    elif request.domain == 'restaurants':
        idx = 'restaurants'
        entity_label = 'restaurant'
    elif request.domain == 'overlooks':
        idx = 'overlooks'
        entity_label = 'overlook'
    elif request.domain == 'hiking':
        idx = 'trails'
        entity_label = 'trail'

    entity_name = _get_entity_name(request, entity_label)

    # kb: knowledge base
    kb = app.question_answerer.get(index=idx, name=entity_name)

    info = kb[0][info_name]

    return entity_name, info
