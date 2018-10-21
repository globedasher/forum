from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

import sys

# Create your models here.

class CatMan(models.Manager):

    def register(self, *args):
        print("Register Manager")
        errors = []
        #print(user)
        try:
            #Try to create a unique category
            print("*args")
            print(*args)
            #print(user)
            name = args[0]["name"]
            print("name")
            print(name)
            created_by = args[1]
            print("created_by")
            print(created_by)
            cat = Category(name=name, created_by=created_by)
            cat.save()
            #return True, cat
        except:
            #Return errors
            print("errors?")
            print(sys.exc_info())
            #return False, errors
        finally:
            print("not here?")

        if errors:
            print("errors!!!")
            return (False, errors)
        else:
            print("returns")
            return (True, cat)




class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    private = models.CharField(max_length=10)
    created_by = models.ForeignKey(User
                            ,on_delete='PROTECT'
                            ,related_name="created")

    objects = CatMan()


class Post(models.Model):
    """
    Posts to the forum.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User
                            ,on_delete='CASCADE'
                            ,related_name="post_owner")

    category = models.ForeignKey('Category'
                                ,on_delete='CASCADE'
                                ,related_name="categories")

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
