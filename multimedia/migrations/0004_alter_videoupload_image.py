# Generated by Django 5.1.4 on 2024-12-20 14:41

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0003_alter_videoupload_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoupload',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=[760, 420], upload_to='videoImage/'),
        ),
    ]