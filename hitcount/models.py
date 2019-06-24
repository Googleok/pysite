
from django.db import models

# Create your models here.
from django.utils import timezone

from board.models import Board


class HitCount(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)
    post = models.ForeignKey(Board, to_field='id', default=None, null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'{self.id}, {self.post}, {self.date}'
