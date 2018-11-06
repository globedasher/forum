# Generated by Django 2.1.2 on 2018-11-06 03:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0003_auto_20181021_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('body', models.CharField(max_length=5000)),
                ('owner', models.ForeignKey(on_delete='CASCADE', related_name='response_owner', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete='CASCADE', related_name='post', to='forum.Post')),
            ],
        ),
    ]
