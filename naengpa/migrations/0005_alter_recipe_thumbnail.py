# Generated by Django 3.2.5 on 2021-07-26 06:33

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('naengpa', '0004_alter_recipe_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(default='', upload_to=''),
        ),
    ]
