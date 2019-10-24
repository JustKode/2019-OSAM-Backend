from django.db import models
from django.contrib.auth.models import User


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    written = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=128)
    summary = models.CharField(max_length=256)
    content = models.TextField()
    
    def __str__(self):
        return "{}{} - {}".format(self.user.first_name, self.user.last_name, self.title)
    
    def save(self, *args, **kwargs):
        self.summary = self.content[:256]
        super().save(*args, **kwargs)