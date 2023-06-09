__all__ = ['Stat','StatBase']

from datetime import datetime

from django.db import models

class Stat(models.Model):
    name = models.TextField(unique=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'commands_stat'
        managed = False

class StatBase(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        db_table = 'commands_stat'
        managed = False
