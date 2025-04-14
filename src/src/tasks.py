from celery import shared_task
from django.db.models.expressions import F, Value
from django.db.transaction import atomic
from django.utils import timezone

from . import models


@shared_task
def schedule_reward(pk: int) -> None:
    with atomic():
        reward = models.ScheduledReward.objects.filter(pk=pk).first()
        if reward is None:
            print(f"Not found ScheduledReward({pk})")
            return

        # Возможно, изменили время награждения и создали новую таску,
        # из-за чего эта стала неактуальна.
        if reward.execute_at > timezone.now():
            print(
                f"Discarding ScheduledReward({pk}) because it's not supposed to be executed yet"
            )
            return

        # Не допускаем ситуации, когда 2 одновременно выполняемые таски
        # изменяют coins пользователя первая с 300 до 500, вторая с 300 до 800.
        # Если бы они так применились, то пользователь бы потерял 200 или 500 coins,
        # что не хорошо.
        models.User.objects.filter(pk=reward.user_id).update(
            coins=F("coins") + Value(reward.amount)
        )

        models.RewardLog.objects.create(
            user=reward.user, amount=reward.amount, given_at=timezone.now()
        )
        reward.delete()
