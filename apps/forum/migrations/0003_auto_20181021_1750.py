# Generated by Django 2.1.2 on 2018-10-21 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20181020_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='private',
            field=models.BooleanField(default=1),
        ),
    ]
