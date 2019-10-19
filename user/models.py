from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    start_date = models.DateField()  # 입대 일자
    end_date = models.DateField()  # 제대 일자
    private_first_class = models.DateField()  # 일병
    corparal = models.DateField()  # 상병
    sergeant = models.DateField()  # 병장
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    say = models.CharField(max_length=128)  # 좌우명
    regular_holiday = models.IntegerField(default=26)  # 정기 휴가
    reward_holiday = models.IntegerField(default=0)  # 포상 휴가
    consolation_holiday = models.IntegerField(default=0)  # 위로 휴가
    used_holiday = models.IntegerField(default=0)  # 사용한 휴가
    checked_holiday = models.IntegerField(default=0)  # 사용 예정 휴가
    
    def __str__(self):
        return "{}{}".format(self.user.first_name, self.user.last_name)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.private_first_class = self.start_date + datetime.timedelta(month=2)
            self.private_first_class.days = 1
            self.corparal = self.private_first_class + datetime.timedelta(month=6)
            self.sergeant = self.corparal + datetime.timedelta(month=6)
        super().save(*args, **kwargs)
        

    