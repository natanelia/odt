# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key_label', models.TextField(max_length=128)),
                ('key', models.TextField()),
                ('value', models.TextField()),
                ('value_label', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='reference',
            unique_together=set([('key_label', 'key', 'value_label')]),
        ),
    ]
