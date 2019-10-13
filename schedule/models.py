from django.db import models
from django.contrib.auth.models import User


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_type = models.IntegerField(default=0)
    title = models.CharField(max_length=64)
    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return "{}{} - {}".format(self.user.first_name, self.user.last_name, self.title)