import sys
import re
from odt import settings
from odt import term_colors as tc
from odt.metadata.core import MetaData

class MetaDataValidator(object):
    NO_MODEL_DOC = 'has no documentation'
    NO_HELP_TEXT = 'has no help text'

    @staticmethod
    def scan_models():
        models = MetaData.find_models()

        model_notices = []
        if len(models):
            for m in models:
                field_warnings = []
                field_errors = []
                for f in m.get_fields():
                    # warn/err for help text inexistence
                    field_notice, notice_level = MetaDataValidator.validate_help_text(f)

                    if notice_level == 1:
                        field_warnings.append(field_notice)
                    elif notice_level == 2:
                        field_errors.append(field_notice)

                model_notice = m.serialize()
                model_notice['warnings'] = {}
                model_notice['errors'] = {}

                model_doc_notice, notice_level = MetaDataValidator.validate_model_doc(m)
                if notice_level == 1:
                    model_notice['warnings']['Model'] = [model_doc_notice]
                elif notice_level == 2:
                    model_notice['errors']['Model'] = [model_doc_notice]


                if len(field_warnings):
                    model_notice['warnings']['Field'] = field_warnings
                
                if len(field_errors):
                    model_notice['errors']['Field'] = field_errors

                
                if len(model_notice['warnings']) or len(model_notice['errors']):
                    model_notices.append(model_notice)

        return model_notices

    @staticmethod
    def validate_model_doc(model):
        notice = model.serialize()
        notice_level = 0
        p = re.compile('\A\w+\((.*)\)\Z', re.MULTILINE)
        m = p.match(model.doc)
        if m:
            notice['reason'] = MetaDataValidator.NO_MODEL_DOC
            notice_level = settings.ODT_NOTICE_LEVEL_NO_MODEL_DOC
        
        return notice, notice_level

    @staticmethod
    def validate_help_text(field):
        notice = field.serialize()
        notice_level = 0
        if field.class_name != 'AutoField' and not field.class_name.endswith('Rel'):
            if not field.help_text:
                notice['reason'] = MetaDataValidator.NO_HELP_TEXT
                notice_level = settings.ODT_NOTICE_LEVEL_NO_HELP_TEXT
        
        return notice, notice_level

    @staticmethod
    def validate():
        notices = MetaDataValidator.scan_models()
        err_counts = 0
        if len(notices):
            for mn in notices:
                add_text = ''
                model_err_count = 0
                model_warn_count = 0
                
                for k, v in mn['warnings'].iteritems():
                    model_warn_count += len(v)

                for k, v in mn['errors'].iteritems():
                    model_err_count += len(v)

                err_counts += model_err_count

                if model_err_count:
                    add_text += tc.color('%d error(s)' % (model_err_count), tc.RED)

                if model_warn_count:
                    add_text += ' and ' if add_text else ''

                    add_text += tc.color('%d warning(s)' % (model_warn_count), tc.BLUE)

                sys.stdout.write('Model %s has %s.\n' % (
                    tc.color(mn['full_name'], tc.BOLD),
                    add_text,
                ))


                for k, v in mn['errors'].iteritems():
                    for notice in v:
                        sys.stdout.write ('  %s %s %s.\n' % (
                            k,
                            tc.color(notice['name'], tc.GREEN),
                            tc.color(notice['reason'], tc.RED)))


                for k, v in mn['warnings'].iteritems():
                    for notice in v:
                        sys.stdout.write ('  %s %s %s.\n' % (
                            k,
                            tc.color(notice['name'], tc.GREEN),
                            tc.color(notice['reason'], tc.YELLOW)))

                sys.stdout.write('\n')
            
            if err_counts:
                raise Exception(tc.color('Model check has found %s error(s).\n\n' % err_counts, tc.RED))
        else:
            sys.stdout.write (tc.color('Model check is done with no errors/warnings.\n\n', tc.GREEN))