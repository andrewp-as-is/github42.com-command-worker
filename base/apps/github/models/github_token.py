__all__ = ['Token','TokenBase']

from datetime import datetime

from django.db import models

"""
https://developer.github.com/v3/rate_limit/
"""


class Token(models.Model):
    user = models.ForeignKey('users.User', related_name='+',on_delete=models.CASCADE)
    token = models.TextField(unique=True)

    is_active = models.BooleanField(default=True)
    rate_remaining = models.IntegerField(null=True)
    rate_used = models.IntegerField(null=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    reset_at = models.DateTimeField(null=True)

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False

    def get_rate_remaining(self):
        if self.is_active:
            return self.rate_remaining if self.rate_remaining is not None else 5000
        return 0

    def update(self,headers):
        Token.objects.filter(id=self.id).update(
            rate_remaining=int(headers.get('X-RateLimit-Remaining')),
            rate_used=int(headers.get('X-RateLimit-Used')),
            reset_at=datetime.utcfromtimestamp(int(headers.get('X-RateLimit-Reset'))),
            updated_at=datetime.now()
        )

class TokenBase(models.Model):
    user = models.ForeignKey('users.User', related_name='+',on_delete=models.CASCADE)
    token = models.TextField(unique=True)

    created_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'github_token'
        managed = False

"""
отзыв токена - revocation
отозван пользователем - revoked
"""
