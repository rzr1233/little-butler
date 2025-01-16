from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
from django.db import transaction


class Command(BaseCommand):
    help = "清理数据库中重复的邮箱账户，保留最早注册的账户"

    def handle(self, *args, **options):
        # 找出所有重复的邮箱
        duplicate_emails = (
            User.objects.values("email")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
            .values_list("email", flat=True)
        )

        if not duplicate_emails:
            self.stdout.write(self.style.SUCCESS("没有发现重复的邮箱账户"))
            return

        self.stdout.write(f"发现 {len(duplicate_emails)} 个重复的邮箱")

        with transaction.atomic():
            for email in duplicate_emails:
                if not email:  # 跳过空邮箱
                    continue

                # 获取该邮箱的所有用户，按注册时间排序
                users = User.objects.filter(email=email).order_by("date_joined")

                # 保留最早注册的账户
                keep_user = users.first()
                delete_users = users.exclude(id=keep_user.id)

                self.stdout.write(
                    f"邮箱 {email}:"
                    f"\n  - 保留用户: {keep_user.username} (ID: {keep_user.id})"
                    f"\n  - 删除用户: {', '.join([u.username for u in delete_users])}"
                )

                # 删除其他账户
                delete_users.delete()

        self.stdout.write(self.style.SUCCESS("重复邮箱清理完成"))
