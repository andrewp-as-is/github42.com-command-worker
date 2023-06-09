from datetime import datetime

from django.db import models
from django.utils.timesince import timesince

class BaseSync(models.Model):
    login = models.TextField(unique=True)
    user_id = models.IntegerField()
    token_id = models.IntegerField()
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    @property
    def is_completed(self):
        return False not in list(map(lambda f:f.value_from_object(self),self._meta.fields))

    @property
    def is_disabled(self):
        if self.started_at:
            td = (datetime.now()-self.started_at)
            if self.is_completed:
                return td.total_seconds()<20
            else:
                return td.total_seconds()<60*2
        return False

    def __str__(self):
        if self.is_completed:
            td = datetime.now()-self.finished_at
            ts = timesince(self.finished_at)
            if td.total_seconds()<60:
                ts = '%s seconds' % int(td.total_seconds())
            return 'updated %s ago' % ts.split(',')[0]
        else:
            if not self.started_at:
                return ''
            td = datetime.now()-self.started_at
            ts = timesince(self.started_at)
            if td.total_seconds()<60:
                ts = '%s seconds' % int(td.total_seconds())
            return 'started %s ago' % ts.split(',')[0] if td.total_seconds()>=2 else ''

