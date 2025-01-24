from django.db import models
from django.contrib.auth.models import User
from accounts.models import Family


class Account(models.Model):
    """账本模型"""

    TYPE_CHOICES = [
        ("personal", "个人"),
        ("family", "家庭"),
    ]

    name = models.CharField("账本名称", max_length=100)
    type = models.CharField("类型", max_length=20, choices=TYPE_CHOICES)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_accounts"
    )
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, null=True, blank=True, related_name="accounts"
    )
    description = models.TextField("描述", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "账本"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    """账单分类模型"""

    TYPE_CHOICES = [
        ("expense", "支出"),
        ("income", "收入"),
    ]

    name = models.CharField("分类名称", max_length=50)
    type = models.CharField("类型", max_length=20, choices=TYPE_CHOICES)
    icon = models.CharField("图标", max_length=50, blank=True)  # 存储图标的类名或代码
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "账单分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_type_display()}-{self.name}"


class Bill(models.Model):
    """账单模型"""

    TYPE_CHOICES = [
        ("income", "收入"),
        ("expense", "支出"),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="bills",
        verbose_name="所属账本",
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="类型",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="金额",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="分类",
    )
    date = models.DateTimeField(
        verbose_name="日期时间",
    )
    description = models.TextField(
        blank=True,
        verbose_name="备注",
    )
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        verbose_name="创建者",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        verbose_name = "账单"
        verbose_name_plural = verbose_name
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_type_display()}-{self.amount}"


class Budget(models.Model):
    """预算模型"""

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="budgets"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField("预算金额", max_digits=10, decimal_places=2)
    start_date = models.DateField("开始日期")
    end_date = models.DateField("结束日期")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "预算"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.account.name} - {self.category.name} ({self.start_date} ~ {self.end_date})"
