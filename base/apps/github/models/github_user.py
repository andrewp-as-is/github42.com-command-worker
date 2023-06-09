__all__ = ['User','UserBase']

from django.db import models

"""
https://developer.github.com/v3/users/
"""

class UserMixin:
    def get_absolute_url(self):
        return '/' + self.login

class User(UserMixin,models.Model):
    id = models.BigAutoField(primary_key=True)
    login = models.CharField(max_length=39,unique=True)
    type = models.CharField(max_length=100,null=True,blank=True)
    name = models.TextField(null=True,blank=True)
    company = models.TextField(null=True,blank=True)
    blog = models.TextField(null=True,blank=True)
    location = models.TextField(null=True,blank=True)
    bio = models.TextField(null=True,blank=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    public_repos_count = models.IntegerField(null=True)
    private_repos_count = models.IntegerField(null=True)
    public_stars_count = models.IntegerField(null=True)
    private_stars_count = models.IntegerField(null=True)

    followers_count = models.IntegerField(null=True)
    following_count = models.IntegerField(null=True)

    # types
    public_count = models.IntegerField(null=True)
    private_count = models.IntegerField(null=True)
    sources_count = models.IntegerField(null=True)
    forks_count = models.IntegerField(null=True)
    archived_count = models.IntegerField(null=True)
    mirrors_count = models.IntegerField(null=True)

    class Meta:
        db_table = 'github_user'
        managed = False

    def get_absolute_url(self):
        return '/' + self.login

    def get_avatar_url(self):
        return 'https://github.com/%s.png' % (self.login,)

class UserBase(UserMixin,models.Model):
    login = models.CharField(max_length=39,unique=True)
    type = models.CharField(max_length=100)

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False
