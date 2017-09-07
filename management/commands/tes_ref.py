from django.core.management.base import BaseCommand, CommandError

from odt.metadata.core import MetaData
from odt.models import Reference, ReferencingTest
from odt.reference import ReferenceField, ReferenceObject, ValueRef, LabelRef

class Command(BaseCommand):
    def handle(self, *args, **options):
        # ref = Reference.objects.get(key_label='state_code', key='CA', value='California', value_label='state_name')
        ref = ReferenceObject('state_code', 'CA', 'California', 'state_name')
        ref.save()

        a = ReferencingTest.objects.all()
        for b in a:
            b.state = LabelRef('state_code', 'CA')
            b.save()
            b.refresh_from_db()
            print b.state.convertTo('state_code')