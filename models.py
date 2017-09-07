from django.db import models

class Reference(models.Model):
    '''
    Reference Table used to contain all references defined in all apps.
    '''
    key_label = models.TextField(blank=False, null=False, unique=False, max_length=128, help_text='The label for the value keys, or in other words, the Reference Category')
    key = models.TextField(blank=False, null=False, unique=False, help_text='The key for the values.')
    value = models.TextField(blank=False, null=False, unique=False, help_text='The value for a key')
    value_label = models.TextField(blank=False, null=False, unique=False, help_text='The label for the value, or in other words, the Value Domain of a key')

    class Meta:
        unique_together = (('key_label', 'key', 'value_label'))

    def __str__(self):
        return self.value