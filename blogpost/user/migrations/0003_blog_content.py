# Generated by Django 4.2.7 on 2023-11-22 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
