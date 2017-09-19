import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render

from .metadata.core import MetaData
from .metadata.validator import MetaDataValidator

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@csrf_exempt
def index(request):
    models = MetaData.find_models(
        model_name=request.GET.get('model_name'), 
        field_name=request.GET.get('field_name'),
        field_help_text=request.GET.get('field_help_text'),
    )

    config = None
    if request.method == 'POST' and request.FILES['config']:
        config_file = request.FILES['config']
        config = json.load(config_file)

    context = {
        'models': models,
        'query': {
            'model_name': request.GET.get('model_name'),
            'field_name': request.GET.get('field_name'),
            'field_help_text': request.GET.get('field_help_text'),
        },
        'config': config,
    }
    return render(request, 'odt/index.html', context)

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def generate_config(request):
    queries = request.POST
    query_dict = {}
    for q, v in queries.iteritems():
        if '|' in q:
            
            splitted = q.split('|')
            query_dict[splitted[0]] = query_dict.get(splitted[0], {})
            query_dict[splitted[0]][splitted[1]] = True
        else:
            query_dict[q] = query_dict.get(q, {})
            query_dict[q]['_'] = True
    resp = JsonResponse(query_dict)
    resp['Content-Disposition'] = 'attachment; filename=odt_config.json'
    return resp
