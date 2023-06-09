__all__ = ['RepoStar']

from django.db import models

"""
https://developer.github.com/v3/activity/starring/
"""

class RepoStar(models.Model):
    user = models.ForeignKey('User',related_name='github_starred_repo', on_delete=models.CASCADE)
    repo = models.ForeignKey('Repo', on_delete=models.CASCADE)
    starred_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'github_repo_star'
        managed = False
        unique_together = ('user', 'repo',)
