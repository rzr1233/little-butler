from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """用户档案模型"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField("昵称", max_length=50, blank=True)
    avatar = models.CharField("头像", max_length=255, blank=True, null=True, default="")
    bio = models.TextField("个人简介", max_length=500, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "用户档案"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}的档案"


class Family(models.Model):
    """家庭组模型"""

    name = models.CharField("家庭名称", max_length=100)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_families"
    )
    members = models.ManyToManyField(
        User, through="FamilyMember", related_name="families"
    )
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "家庭"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class FamilyMember(models.Model):
    """家庭成员关系模型"""

    ROLE_CHOICES = [
        ("admin", "管理员"),
        ("member", "成员"),
    ]

    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        "角色", max_length=20, choices=ROLE_CHOICES, default="member"
    )
    joined_at = models.DateTimeField("加入时间", auto_now_add=True)

    class Meta:
        verbose_name = "家庭成员"
        verbose_name_plural = verbose_name
        unique_together = ["family", "user"]

    def __str__(self):
        return f"{self.user.username} - {self.family.name} ({self.get_role_display()})"
