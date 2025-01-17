from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from bills.models import Bill, Account
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json


def format_month_to_chinese(date):
    """将日期格式化为中文月份"""
    return f"{date.year}年{date.month}月"


class StatsHomeView(LoginRequiredMixin, TemplateView):
    """统计分析首页"""

    template_name = "stats/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get("account_id")
        account = Account.objects.get(id=account_id)
        context["account"] = account

        # 获取账单数据
        bills = Bill.objects.filter(account=account)

        # 生成趋势图
        trend_chart = self.generate_trend_chart(bills)
        context["trend_chart"] = trend_chart

        # 生成分类占比图
        category_chart = self.generate_category_chart(bills)
        context["category_chart"] = category_chart

        # 获取月度统计
        monthly_stats = self.get_monthly_stats(bills)
        context["monthly_stats"] = monthly_stats

        # 获取年度统计
        yearly_stats = self.get_yearly_stats(bills)
        context["yearly_stats"] = yearly_stats

        return context

    def generate_trend_chart(self, bills):
        """生成收支趋势图"""
        # 按月份统计收支
        monthly_data = (
            bills.annotate(month=TruncMonth("date"))
            .values("month", "type")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        # 转换为DataFrame
        df = pd.DataFrame(monthly_data)
        if df.empty:
            return None

        # 将月份转换为中文格式
        df["month_label"] = df["month"].apply(format_month_to_chinese)

        # 数据透视
        df_pivot = df.pivot(index="month", columns="type", values="total").fillna(0)
        month_labels = df["month_label"].unique()

        # 创建图表
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=month_labels,
                y=df_pivot["income"],
                name="收入",
                line=dict(color="#28a745"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=month_labels,
                y=df_pivot["expense"],
                name="支出",
                line=dict(color="#dc3545"),
            )
        )

        # 更新布局
        fig.update_layout(
            title="月度收支趋势",
            xaxis_title="月份",
            yaxis_title="金额",
            template="plotly_white",
            height=400,
            xaxis=dict(tickangle=45),  # 倾斜x轴标签以防重叠
            margin=dict(t=50, b=50, l=50, r=50),  # 调整边距
        )

        return fig.to_html(
            full_html=False,
            include_plotlyjs=False,  # 不包含 Plotly.js，因为我们在模板中已经加载了
            config={"displayModeBar": False},
        )

    def generate_category_chart(self, bills):
        """生成分类占比图"""
        # 获取支出分类数据
        category_data = (
            bills.filter(type="expense")
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        # 转换为DataFrame
        df = pd.DataFrame(category_data)
        if df.empty:
            return None

        # 创建饼图
        fig = px.pie(
            df,
            values="total",
            names="category__name",
            title="支出分类占比",
            labels={"category__name": "分类", "total": "金额"},
        )

        # 更新布局
        fig.update_layout(
            height=400,
            showlegend=True,
            margin=dict(t=50, b=50, l=50, r=50),  # 调整边距
        )

        return fig.to_html(
            full_html=False,
            include_plotlyjs=False,  # 不包含 Plotly.js，因为我们在模板中已经加载了
            config={"displayModeBar": False},
        )

    def get_monthly_stats(self, bills):
        """获取月度统计数据"""
        current_month = datetime.now().replace(day=1)
        last_month = (current_month - timedelta(days=1)).replace(day=1)

        # 本月数据
        current_month_stats = {
            "income": bills.filter(
                type="income",
                date__year=current_month.year,
                date__month=current_month.month,
            ).aggregate(total=Sum("amount"))["total"]
            or 0,
            "expense": bills.filter(
                type="expense",
                date__year=current_month.year,
                date__month=current_month.month,
            ).aggregate(total=Sum("amount"))["total"]
            or 0,
        }

        # 上月数据
        last_month_stats = {
            "income": bills.filter(
                type="income", date__year=last_month.year, date__month=last_month.month
            ).aggregate(total=Sum("amount"))["total"]
            or 0,
            "expense": bills.filter(
                type="expense", date__year=last_month.year, date__month=last_month.month
            ).aggregate(total=Sum("amount"))["total"]
            or 0,
        }

        return {"current": current_month_stats, "last": last_month_stats}

    def get_yearly_stats(self, bills):
        """获取年度统计数据"""
        current_year = datetime.now().year

        # 年度总计
        yearly_total = {
            "income": bills.filter(type="income", date__year=current_year).aggregate(
                total=Sum("amount")
            )["total"]
            or 0,
            "expense": bills.filter(type="expense", date__year=current_year).aggregate(
                total=Sum("amount")
            )["total"]
            or 0,
        }

        # 月均数据
        monthly_avg = {
            "income": yearly_total["income"] / 12,
            "expense": yearly_total["expense"] / 12,
        }

        return {"total": yearly_total, "monthly_avg": monthly_avg}
