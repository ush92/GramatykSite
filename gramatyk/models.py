from django.db import models
from django.contrib.auth.models import User


class Solution(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    is_public = models.BooleanField()
    grammar = models.TextField()
    user = models.ForeignKey(User)
    likes = models.IntegerField()
