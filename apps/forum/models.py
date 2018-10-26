from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

import sys

# Create your models here.

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    private = models.BooleanField(default=1)
    created_by = models.ForeignKey(User
                            ,on_delete='PROTECT'
                            ,related_name="created")



class Post(models.Model):
    """
    Posts to the forum.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User
                            ,on_delete='CASCADE'
                            ,related_name="post_owner"
                            )

    category = models.ForeignKey(Category
                                ,on_delete='CASCADE'
                                ,related_name="categories"
                                )

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
