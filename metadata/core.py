from django.contrib.contenttypes.models import ContentType
from odt import settings
from odt.metadata.info import ModelInfo, FieldInfo

'''
Bayangkan Anda seorang DB Admin sedang ingin merancang tabel baru.
Metadata apa yang Anda butuhkan?

>> Search
    Melakukan pencarian model berdasarkan:
    - Nama model
    - Nama field
    - Isi help text
'''


class MetaData(object):
    @staticmethod
    def all_models():
        models = []
        for ct in ContentType.objects.all():
            if ct.model_class():
                models.append(ModelInfo(ct.model_class()))

        return models

    @staticmethod
    def find_models(model_name='', field_name='', field_help_text=''):
        model_name = model_name or ''
        field_name = field_name or ''
        field_help_text = field_help_text or ''

        models = MetaData.all_models()
        models_filtered_by_apps = []
        models_filtered_by_model_name = []
        models_filtered_by_field_name = []
        models_filtered_by_field_help_text = []
        result = models
        
        if len(settings.ODT_IGNORE_APPS):
            for m in result:
                found = False
                for ignored in settings.ODT_IGNORE_APPS:
                    if m.full_name.lower().startswith(ignored.lower()):
                        found = True
                
                if not found:
                    models_filtered_by_apps.append(m)
            
            result = models_filtered_by_apps

        if model_name != '':
            for m in result:
                if m.full_name.lower().find(model_name.lower()) > -1:
                    models_filtered_by_model_name.append(m)
            
            result = models_filtered_by_model_name
        
        if field_name != '':
            for m in result:
                for field in m.get_fields():
                    if field.name.lower().find(field_name.lower()) > - 1:
                        models_filtered_by_field_name.append(m)
        
            result = models_filtered_by_field_name    
        
        if field_help_text != '':
            for m in result:
                for field in m.get_fields():
                    if field.help_text:
                        if field.help_text.lower().find(field_help_text.lower()) > - 1:
                            models_filtered_by_field_help_text.append(m)
        
            result = models_filtered_by_field_help_text               

        return result