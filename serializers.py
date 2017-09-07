from odt.reference import ReferenceObject
from rest_framework import serializers

class ReferenceField(serializers.Field):
    '''
    Reference object is serialized into 'key_label||key||value||value_label'
    '''

    def to_representation(self, obj):
        return '%s||%s||%s||%s' % (obj.key_label, obj.key, obj.value, obj.value_label)

    def to_internal_value(self, data):
        key_label, key, value, value_label = [c for c in data.split('||')]
        return ReferenceObject(key_label, key, value, value_label)