# Generated by Django 5.0.7 on 2024-07-31 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ironSwordsApp', '0005_remove_hero_description_hero_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='heroes/'),
        ),
    ]
