from django.db import models

class Recording(models.Model):
    session_id = models.CharField(max_length=255)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)