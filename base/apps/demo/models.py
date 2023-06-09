from django.db import models

class DemoOrg(models.Model):
    login = models.TextField(unique=True)

    class Meta:
        db_table = 'demo_org'
        managed = False

class DemoUser(models.Model):
    login = models.TextField(unique=True)

    class Meta:
        db_table = 'demo_user'
        managed = False
