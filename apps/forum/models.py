from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    private = models.CharField(max_length=10)


class Post(models.Model):
    """
    Posts to the forum.
    """
    owner = models.ForeignKey(User
                            ,on_delete='CASCADE'
                            ,related_name="post_owner")

    category = models.ForeignKey('Category'
                                ,on_delete='CASCADE'
                                ,related_name="categories")

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
