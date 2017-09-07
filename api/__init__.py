from django.apps import apps
from django.db import models
from rest_framework import serializers, routers, viewsets
from odt.metadata.core import MetaData
from odt.reference import ReferenceField
from odt import serializers as ODT_serializers
from odt.settings import *
from django_filters.rest_framework import DjangoFilterBackend


import pprint

pp = pprint.PrettyPrinter(indent=2)

router = routers.DefaultRouter()
model_classes = []
viewset_classes = []

model_infos = MetaData.find_models()

for m in model_infos:
    paths = m.full_name.split('.')
    parent_module = paths[0]
    exec('%s = __import__("%s")' % (paths[0], paths[0]))

    clean_path = ''
    for p in paths:
        clean_path += p.capitalize()

    field_names = []
    foreign_fields = []
    reference_fields = {}
    for f in m.get_fields():
        if isinstance(f.field, models.Field) or issubclass(f.field.__class__, models.Field):
            f_ser = f.serialize()
            is_ignored = False
            for ignored in ODT_IGNORE_APPS:
                if f_ser['class_path'].startswith(ignored) and not ignored.startswith('django'):
                    is_ignored = True

            if (f_ser['class_path'] == 'django.db.models.fields.related'):
                for ignored in ODT_IGNORE_APPS:
                    if f_ser['related_model_path'].startswith(ignored):
                        is_ignored = True

            for ignored in ODT_IGNORE_APPS:
                if f_ser.get('through', '').startswith(ignored):
                    is_ignored = True

            if isinstance(f.field, ReferenceField):
                reference_fields[f_ser['name']] = ODT_serializers.ReferenceField()

            if not is_ignored:
                field_names.append(f.name)

            if f.class_path == 'django.db.models.fields.related':
                foreign_fields.append(f)


    cls_attrs =  {
        'Meta': type('Meta', (object,), {
            'model': eval(m.full_name),
            'fields': tuple(field_names),
        }),
        'model_full_name': m.full_name,
        'foreign_fields': foreign_fields,
        'clean_path': clean_path,
    }
    cls_attrs.update(reference_fields)

    new_serializer_class = type('%sSerializer' % clean_path, (serializers.ModelSerializer,), cls_attrs)

    model_classes.append(new_serializer_class)


for ser_class in model_classes:
    url = ser_class.model_full_name.lower().replace('.','/')

    new_viewset_class = type('%sViewSet' % ser_class.clean_path, (viewsets.ModelViewSet,), {
        'queryset': eval(ser_class.model_full_name).objects.all(),
        'serializer_class': ser_class,
        'filter_backends': (DjangoFilterBackend,),
        'filter_fields': ser_class.Meta.fields,
        'pagination_class': None,
    })

    viewset_classes.append((url, new_viewset_class,))

for url, vc in viewset_classes:
    router.register(url, vc)
