from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    start_date = models.DateField()  # 입대 일자
    end_date = models.DateField()  # 제대 일자
    private_first_class = models.DateField(null=True)  # 일병
    corparal = models.DateField(null=True)  # 상병
    sergeant = models.DateField(null=True)  # 병장
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
        list_var = list(map(lambda x: int(x), self.start_date.split('-')))
        pfc_list = [list_var[0] + (list_var[1] + 2) // 13, (list_var[1] - 1 + 2) % 12 + 1, 1]
        cp_list = [pfc_list[0] + (pfc_list[1] + 6) // 13, (pfc_list[1] - 1 + 6) % 12 + 1, 1]
        sg_list = [cp_list[0] + (cp_list[1] + 6) // 13, (cp_list[1] - 1 + 6) % 12 + 1, 1]

        self.private_first_class = '-'.join(list(map(lambda x: '%02d' % x, pfc_list)))
        self.corparal = '-'.join(list(map(lambda x: '%02d' % x, cp_list)))
        self.sergeant = '-'.join(list(map(lambda x: '%02d' % x, sg_list)))

        super().save(*args, **kwargs)
        

    