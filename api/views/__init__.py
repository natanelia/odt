from django.http import JsonResponse, HttpResponse
from odt.metadata.core import MetaData
from odt.settings import *

def model_sync(request):
    model_infos = MetaData.find_models()
    serialized_model_infos = []

    for m in model_infos:
        sm = m.serialize_with_fields()

        marked_delete = []
        for f in sm['fields']:
            for ignored in ODT_IGNORE_APPS:
                if f['class_path'].startswith(ignored) and not ignored.startswith('django'):
                    marked_delete.append(f['name'])

            if (f['class_path'] == 'django.db.models.fields.related'):
                for ignored in ODT_IGNORE_APPS:
                    if f['related_model_path'].startswith(ignored):
                        marked_delete.append(f['name'])

            for ignored in ODT_IGNORE_APPS:
                if f.get('through', '').startswith(ignored):
                    marked_delete.append(f['name'])

            if (f['class_path'] == 'django.db.models.fields.related' \
                and 'Rel' in f['class_name']) \
            or (f['class_path'] == 'django.db.models.fields' \
                and f['class_name'] == 'AutoField'):

                marked_delete.append(f['name'])


        sm['fields'][:] = [f for f in sm['fields'] \
            if not (f['name'] in marked_delete)]
        serialized_model_infos.append(sm)

    return JsonResponse(serialized_model_infos, safe=False)
