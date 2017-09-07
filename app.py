from django.apps import AppConfig
from odt.metadata.core import MetaData
from odt.metadata.validator import MetaDataValidator

class ODTConfig(AppConfig):
    name = 'odt'
    verbose_name = 'ODT Server'
    def ready(self):
        MetaDataValidator.validate()
