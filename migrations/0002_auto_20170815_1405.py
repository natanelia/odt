# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='key',
            field=models.TextField(help_text=b'The key for the values.'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='key_label',
            field=models.TextField(help_text=b'The label for the value keys, or in other words, the Reference Category', max_length=128),
        ),
        migrations.AlterField(
            model_name='reference',
            name='value',
            field=models.TextField(help_text=b'The value for a key'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='value_label',
            field=models.TextField(help_text=b'The label for the value, or in other words, the Value Domain of a key'),
        ),
    ]
