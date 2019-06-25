from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.utils import timezone

from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    hit = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, {self.content}, {self.hit}, {self.groupno}, {self.orderno}, {self.depth}, {self.user}'


class HitCount(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)
    post = models.ForeignKey(Board, to_field='id', default=None, null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'{self.id}, {self.post}, {self.date}'
