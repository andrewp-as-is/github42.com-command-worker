__all__ = ['RepoTopic']

from django.db import models

class RepoTopic(models.Model):
    repo = models.ForeignKey('Repo', on_delete=models.CASCADE)
    slug = models.TextField()

    class Meta:
        db_table = 'github_repo_topic'
        managed = False
        unique_together = [('repo', 'slug')]
