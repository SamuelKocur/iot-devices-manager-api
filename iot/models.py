from django.db import models


class Messages(models.Model):
    topic = models.CharField(max_length=30)
    message = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)

