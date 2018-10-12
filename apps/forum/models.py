from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.


class Post(models.Model):
    """
    Posts to the forum.
    """
    owner = models.ForeignKey(User, on_delete='CASCADE', related_name="org_owner")
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
