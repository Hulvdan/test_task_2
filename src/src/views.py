from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, tasks

User = get_user_model


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    class ProfileResponse(serializers.ModelSerializer):
        class Meta:
            model = models.User
            fields = ("username", "email", "coins")

    @extend_schema(responses={200: OpenApiResponse(response=ProfileResponse)})
    def get(self, request, format=None):
        return Response(self.ProfileResponse(request.user).data)


class RewardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RewardLog
        fields = ("amount", "given_at")


class RewardsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    class RewardsResponse(serializers.Serializer):
        rewards = serializers.ListSerializer(child=RewardLogSerializer())

    @extend_schema(responses={200: OpenApiResponse(response=RewardsResponse)})
    def get(self, request, format=None):
        qs = models.RewardLog.objects.all().filter(user=request.user).order_by("-pk")
        return Response(self.RewardsResponse({"rewards": qs}).data)


class RequestRewardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    SECONDS_IN_DAY = 24 * 60 * 60

    class RequestRewardIsOnCooldown(APIException):
        status_code = 429
        default_detail = "You can request a reward only once a day"
        default_code = "request_reward_is_on_cooldown"

    def post(self, request, format=None):
        if request.user.last_time_asked_reward is not None:
            delta = timezone.now() - request.user.last_time_asked_reward
            if delta.total_seconds() < self.SECONDS_IN_DAY:
                raise self.RequestRewardIsOnCooldown

        # Пользователь не сможет получить несколько наград,
        # параллельно отправив кучу запросов на /api/rewards/request/.
        changed = models.User.objects.filter(
            pk=request.user.pk, last_time_asked_reward=request.user.last_time_asked_reward
        ).update(last_time_asked_reward=timezone.now())

        if changed:
            delta = timedelta(minutes=5)
            obj = models.ScheduledReward.objects.create(
                user=request.user,
                amount=500,
                execute_at=timezone.now() + delta,
            )
            tasks.schedule_reward.apply_async((obj.pk,), countdown=delta.total_seconds())

        return Response()
