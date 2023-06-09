__all__ = ['Repo']

from django.db import models
from django.contrib.postgres.search import SearchVectorField


class Repo(models.Model):
    id = models.BigAutoField(primary_key=True)

    owner_id = models.IntegerField()

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    full_name = models.CharField(max_length=140)
    parent_full_name = models.TextField(null=True)

    description = models.TextField(null=True)
    default_branch = models.TextField(null=True)

    forks_count = models.IntegerField(null=True)
    stargazers_count = models.IntegerField(null=True)
    #watchers_count = models.IntegerField(null=True)
    open_issues_count = models.IntegerField(null=True)

    homepage = models.TextField(null=True)
    language_key = models.TextField(null=True)
    language_name = models.TextField(null=True)
    license_key = models.TextField(null=True)
    license_name = models.TextField(null=True)
    license_spdx_id = models.TextField(null=True)
    mirror_url = models.TextField(null=True)
    size = models.BigIntegerField(null=True)

    is_archived = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_fork = models.BooleanField(default=False)
    is_mirror = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_source = models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True) # updated_at - new stargazers, forks, issues, etc
    pushed_at = models.DateTimeField(null=True)

    # custom:
    contributors_count = models.IntegerField(null=True)
    dependent_repositories_count = models.IntegerField(null=True)
    dependent_packages_count = models.IntegerField(null=True)

    topics = models.TextField(null=True)
    sparkline = models.TextField(null=True)

    class Meta:
        db_table = 'github_repo'
        managed = False

    def get_topics(self):
        return self.topics.split(',') if self.topics else []

    @property
    def login(self):
        return self.full_name.split('/')[0]
