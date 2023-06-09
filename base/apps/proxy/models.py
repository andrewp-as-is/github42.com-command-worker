from django.db import models

class Proxy(models.Model):
    addr = models.TextField(unique=True)
    is_active = models.BooleanField(default=True)
    is_http = models.BooleanField(null=True)
    is_socks4 = models.BooleanField(null=True)
    calls_count = models.IntegerField(default=0,verbose_name='calls')
    errors_count = models.IntegerField(default=0,verbose_name='errors')
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'proxy_proxy'
        managed = False

    def get_proxy_url(self):
        if self.is_socks4:
            return 'socks4://%s' % self.addr
        return 'http://%s' % self.addr

class ProxyBase(models.Model):
    addr = models.TextField(unique=True)
    is_active = models.BooleanField(default=True)
    is_http = models.BooleanField(null=True)
    is_socks4 = models.BooleanField(null=True)

    class Meta:
        db_table = 'proxy_proxy'
        managed = False
