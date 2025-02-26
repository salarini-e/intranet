from django.db import models

class ApacheAccessLog(models.Model):
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    method = models.CharField(max_length=10)
    url = models.TextField()
    protocol = models.CharField(max_length=10)
    status = models.IntegerField()
    size = models.IntegerField()

    def __str__(self):
        return f"{self.ip} - {self.method} {self.url} ({self.status})"
    
class ApacheErrorLog(models.Model):
    timestamp = models.DateTimeField()
    level = models.CharField(max_length=20)
    pid = models.IntegerField()
    tid = models.IntegerField()
    client_ip = models.GenericIPAddressField()
    client_port = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.level} - {self.client_ip} - {self.message}"
