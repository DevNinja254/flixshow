# Generated by Django 5.1.4 on 2024-12-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0002_alter_videosformgenerator_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoupload',
            name='image',
            field=models.ImageField(height_field='420', upload_to='videoImage/', width_field='762'),
        ),
    ]
