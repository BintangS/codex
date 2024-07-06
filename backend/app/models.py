from django.db import models

class Session(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

class Recording(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self):
        return f"Recording for session {self.session.id}"