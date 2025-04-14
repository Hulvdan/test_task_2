from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

from . import models, tasks

UserAdmin.list_display += ("coins",)
UserAdmin.list_filter += ("coins",)
UserAdmin.fieldsets += (("coins", {"fields": ("coins",)}),)

admin.site.register(models.User, UserAdmin)


@admin.register(models.ScheduledReward)
class ScheduledRewardAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "execute_at"]
    ordering = ["-pk"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")

    def save_model(self, request, obj: models.ScheduledReward, form, change):
        super().save_model(request, obj, form, change)

        countdown = (obj.execute_at - timezone.now()).total_seconds()
        tasks.schedule_reward.apply_async((obj.pk,), countdown=countdown)


@admin.register(models.RewardLog)
class RewardLogAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "given_at"]
    readonly_fields = [x.name for x in models.RewardLog._meta.get_fields()]
    ordering = ["-pk"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
