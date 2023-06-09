__all__ = ['UserSync','UserSyncBase']

from datetime import datetime

from django.db import models

from .base import BaseSync


class UserSync(BaseSync):
    is_user_updated = models.BooleanField(default=False)
    is_followers_list_updated = models.BooleanField(default=False)
    is_following_list_updated = models.BooleanField(default=False)
    is_repos_list_updated = models.BooleanField(default=False)
    is_starred_repos_list_updated = models.BooleanField(default=False)
    is_requests_created = models.BooleanField(default=False)

    class Meta:
        db_table = 'github_user_sync'
        managed = False


class UserSyncBase(BaseSync):
    login = models.TextField(unique=True)

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False
"""
    is_user_completed = models.BooleanField(default=False)
    is_followers_completed = models.BooleanField(default=False)
    is_following_completed = models.BooleanField(default=False)
    is_repos_completed = models.BooleanField(default=False)
    is_starred_repos_completed = models.BooleanField(default=False)
"""
