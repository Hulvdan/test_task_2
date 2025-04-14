from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    coins = models.IntegerField(default=0, null=False)
    last_time_asked_reward = models.DateTimeField(null=True)


class ScheduledReward(models.Model):
    user = models.ForeignKey("src.User", on_delete=models.CASCADE)
    amount = models.IntegerField()
    execute_at = models.DateTimeField()


class RewardLog(models.Model):
    user = models.ForeignKey("src.User", on_delete=models.CASCADE)
    amount = models.IntegerField()
    given_at = models.DateTimeField()
