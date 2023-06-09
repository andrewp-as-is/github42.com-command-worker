__all__ = ['UserFollower']


from django.db import models

class UserFollower(models.Model):
    user = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)
    follower = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)

    class Meta:
        db_table = __name__.split('.')[-1]
        managed = False
        unique_together = ('user', 'follower_id',)
