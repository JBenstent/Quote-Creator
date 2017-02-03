from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=155, unique=True)
    birthday = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Quote(models.Model):
    message = models.CharField(max_length=1000)
    author = models.CharField(max_length=55)
    user = models.ForeignKey(User, related_name='userquotes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='usermanyfavorites')
    quote = models.ForeignKey(Quote, related_name='manyfavs')
    favorite = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
