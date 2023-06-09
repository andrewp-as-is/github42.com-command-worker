__all__ = ['RateLimit']

from datetime import datetime, timedelta
from django.db import models


class RateLimit(models.Model):
    created_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'github_rate_limit'
        managed = False

    @property
    def is_exceeded(self):
        return self.created_at>datetime.now()+timedelta(seconds=20)



"""
{
  "documentation_url": "https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#secondary-rate-limits",
  "message": "You have exceeded a secondary rate limit. Please wait a few minutes before you try again."
}

https://docs.github.com/en/rest/overview/resources-in-the-rest-api#secondary-rate-limits
"""
