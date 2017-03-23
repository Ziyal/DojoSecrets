from __future__ import unicode_literals

from django.db import models
from ..login.models import User
from django.db.models import Count


class SecretManager(models.Manager):
    def process_secret(self, postData, user_id):
        secret = Secret.objects.create(post = postData['secret'], creator = User.objects.get(id=user_id))
        return secret

    def process_like(self, postData):
        selected_user = User.objects.get(id = postData['user_id'])
        selected_secret = Secret.objects.get(id = postData['secret_id'])
        selected_secret.like.add(selected_user)
        user_likes = Secret.objects.annotate(num_likes=Count('like'))
        return user_likes

class Secret(models.Model):
    post = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    creator = models.ForeignKey(User, related_name="creator", null=True)
    like = models.ManyToManyField(User, related_name="liked")

    objects = SecretManager()
