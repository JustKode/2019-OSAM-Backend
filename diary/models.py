from django.db import models
from django.contrib.auth.models import User


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    written = models.DateField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return "{}{} - {}".format(self.user.first_name, self.user.last_name, self.title)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)