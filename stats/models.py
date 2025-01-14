from django.db import models
from django.contrib.auth.models import User
from bills.models import Account, Category


class Report(models.Model):
    """统计报告模型"""

    TYPE_CHOICES = [
        ("daily", "日报"),
        ("weekly", "周报"),
        ("monthly", "月报"),
        ("yearly", "年报"),
        ("custom", "自定义"),
    ]

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="reports"
    )
    type = models.CharField("报告类型", max_length=20, choices=TYPE_CHOICES)
    start_date = models.DateField("开始日期")
    end_date = models.DateField("结束日期")
    total_income = models.DecimalField("总收入", max_digits=12, decimal_places=2)
    total_expense = models.DecimalField("总支出", max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "统计报告"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.account.name} {self.get_type_display()} ({self.start_date} ~ {self.end_date})"


class ReportDetail(models.Model):
    """报告明细模型"""

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="details")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField("金额", max_digits=12, decimal_places=2)
    percentage = models.DecimalField(
        "占比", max_digits=5, decimal_places=2
    )  # 存储为百分比，如12.34

    class Meta:
        verbose_name = "报告明细"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.report} - {self.category.name}"
