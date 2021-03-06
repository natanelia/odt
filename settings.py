from django.conf import settings

def get(key, default):
  return getattr(settings, key, default)

ODT_IGNORE_APPS = [] + get('ODT_IGNORE_APPS', ['django'])
ODT_NOTICE_LEVEL_NO_HELP_TEXT = get('ODT_NOTICE_LEVEL_NO_HELP_TEXT', 1)
ODT_NOTICE_LEVEL_NO_MODEL_DOC = get('ODT_NOTICE_LEVEL_NO_MODEL_DOC', 2)
ODT_FIELD_HIDE_WARNINGS = get('ODT_FIELD_HIDE_WARNINGS', 0)
ODT_REFERENCE_IGNORE_MISSING_WARNING = get('ODT_REFERENCE_IGNORE_MISSING_WARNING', False)