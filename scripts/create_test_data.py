import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random
from django.db import models

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookkeeping.settings")
django.setup()

from django.contrib.auth.models import User
from bills.models import Account, Category, Bill, Budget
from accounts.models import Family, FamilyMember
from django.utils import timezone


def create_test_data():
    # 1. 获取或创建测试用户
    user, created = User.objects.get_or_create(
        username="testuser", defaults={"email": "809854538@qq.com", "is_active": True}
    )
    if created:
        user.set_password("testuser123")  # 设置默认密码
        user.save()
        print(f"创建测试用户: testuser (密码: testuser123)")
    else:
        print("使用已存在的测试用户: testuser")

    # 2. 创建家庭
    family, _ = Family.objects.get_or_create(
        name="我的家庭",
        creator=user,
    )
    FamilyMember.objects.get_or_create(family=family, user=user, role="admin")

    # 3. 创建账本
    family_account, _ = Account.objects.get_or_create(
        name="家庭账本",
        type="family",
        owner=user,
        family=family,
        description="全家人共同使用的账本",
    )

    personal_account, _ = Account.objects.get_or_create(
        name="个人账本", type="personal", owner=user, description="个人日常开销账本"
    )

    # 4. 创建分类
    expense_categories = {
        "餐饮": ["早餐", "午餐", "晚餐", "零食", "外卖"],
        "交通": ["公交地铁", "打车", "加油", "停车费"],
        "购物": ["日用品", "衣服", "电子产品"],
        "居住": ["房租", "水电费", "物业费", "网费"],
        "娱乐": ["电影", "游戏", "运动"],
        "医疗": ["药品", "就医", "保健"],
        "教育": ["学费", "书籍", "培训"],
    }

    income_categories = {
        "工资": ["月薪", "奖金", "加班费"],
        "投资": ["股票", "基金", "理财"],
        "其他": ["红包", "报销", "兼职"],
    }

    # 创建支出分类
    for main_cat, sub_cats in expense_categories.items():
        for sub_cat in sub_cats:
            Category.objects.get_or_create(
                name=f"{main_cat}-{sub_cat}", type="expense", account=family_account
            )
            Category.objects.get_or_create(
                name=f"{main_cat}-{sub_cat}", type="expense", account=personal_account
            )

    # 创建收入分类
    for main_cat, sub_cats in income_categories.items():
        for sub_cat in sub_cats:
            Category.objects.get_or_create(
                name=f"{main_cat}-{sub_cat}", type="income", account=family_account
            )
            Category.objects.get_or_create(
                name=f"{main_cat}-{sub_cat}", type="income", account=personal_account
            )

    # 5. 生成最近两年的账单数据
    end_date = timezone.now()
    start_date = end_date - timedelta(days=730)  # 两年的数据
    current_date = start_date

    # 固定支出项（每月）- 添加年度通货膨胀
    def get_monthly_expenses(date):
        inflation = 1 + (date - start_date).days / 365 * 0.03  # 每年3%的通货膨胀
        return [
            ("居住-房租", Decimal(str(round(3000 * inflation, 2)))),
            (
                "居住-水电费",
                Decimal(str(round(250 + random.uniform(-50, 100), 2))),
            ),  # 水电费随季节波动
            ("居住-物业费", Decimal("200.00")),
            ("居住-网费", Decimal("100.00")),
            (
                "教育-培训",
                (
                    Decimal(str(round(1000 * inflation, 2)))
                    if date.month in [3, 9]
                    else Decimal("0.00")
                ),
            ),  # 每学期的培训费
        ]

    # 固定收入项（每月）- 考虑年终奖和加薪
    def get_monthly_incomes(date):
        base_salary = Decimal("15000.00")
        yearly_increase = Decimal("1") + Decimal(
            str((date - start_date).days / 365 * 0.05)
        )  # 每年5%的涨薪
        current_salary = (base_salary * yearly_increase).quantize(Decimal("0.01"))

        incomes = [("工资-月薪", current_salary)]

        # 每月的绩效奖金（1000-3000之间波动）
        bonus = Decimal(str(round(random.uniform(1000, 3000), 2)))
        incomes.append(("工资-奖金", bonus))

        # 年终奖（12月发放）
        if date.month == 12:
            year_end_bonus = current_salary * Decimal(
                str(random.uniform(2, 4))
            )  # 2-4个月的年终奖
            incomes.append(("工资-年终奖", year_end_bonus.quantize(Decimal("0.01"))))

        # 偶尔的投资收入
        if random.random() < 0.2:  # 20%概率有投资收入
            investment_return = Decimal(str(round(random.uniform(1000, 5000), 2)))
            incomes.append(("投资-理财", investment_return))

        return incomes

    # 确保所有固定支出和收入的分类都存在
    all_fixed_expenses = set()
    all_fixed_incomes = set()

    # 收集所有可能的固定支出分类
    test_date = start_date
    while test_date <= end_date:
        for expense_name, _ in get_monthly_expenses(test_date):
            all_fixed_expenses.add(expense_name)
        for income_name, _ in get_monthly_incomes(test_date):
            all_fixed_incomes.add(income_name)
        test_date += timedelta(days=30)

    # 创建所有固定支出分类
    for expense_name in all_fixed_expenses:
        Category.objects.get_or_create(
            name=expense_name, type="expense", account=family_account
        )
        Category.objects.get_or_create(
            name=expense_name, type="expense", account=personal_account
        )

    # 创建所有固定收入分类
    for income_name in all_fixed_incomes:
        Category.objects.get_or_create(
            name=income_name, type="income", account=family_account
        )
        Category.objects.get_or_create(
            name=income_name, type="income", account=personal_account
        )

    # 随机支出概率（根据日期调整）
    def get_expense_probability(date):
        # 周末消费概率更高
        if date.weekday() >= 5:  # 周六日
            return 0.9
        # 月初月末消费概率更高
        elif date.day in [1, 2, 3, 28, 29, 30, 31]:
            return 0.8
        # 发工资后消费概率更高
        elif date.day in [15, 16, 17]:
            return 0.85
        else:
            return 0.6

    # 消费金额范围（根据类别调整）
    expense_ranges = {
        "餐饮": (Decimal("20.00"), Decimal("200.00")),
        "交通": (Decimal("5.00"), Decimal("100.00")),
        "购物": (Decimal("50.00"), Decimal("1000.00")),
        "娱乐": (Decimal("100.00"), Decimal("500.00")),
        "医疗": (Decimal("100.00"), Decimal("2000.00")),
        "教育": (Decimal("50.00"), Decimal("300.00")),
    }

    while current_date <= end_date:
        # 每月固定支出
        if current_date.day == 1:
            for expense_name, amount in get_monthly_expenses(current_date):
                if amount > Decimal("0"):  # 只创建金额大于0的支出
                    category = Category.objects.get(
                        name=expense_name, type="expense", account=family_account
                    )
                    Bill.objects.create(
                        account=family_account,
                        type="expense",
                        amount=amount,
                        category=category,
                        date=current_date,
                        description=f"{current_date.strftime('%Y年%m月')}的{category.name}",
                        created_by=user,
                    )

        # 每月固定收入
        if current_date.day == 15:
            for income_name, amount in get_monthly_incomes(current_date):
                category = Category.objects.get(
                    name=income_name, type="income", account=family_account
                )
                Bill.objects.create(
                    account=family_account,
                    type="income",
                    amount=amount,
                    category=category,
                    date=current_date,
                    description=f"{current_date.strftime('%Y年%m月')}的{category.name}",
                    created_by=user,
                )

        # 随机日常支出
        daily_expense_prob = get_expense_probability(current_date)

        # 家庭账本支出
        if random.random() < daily_expense_prob:
            # 每天可能有多笔支出
            num_expenses = random.randint(1, 3)
            for _ in range(num_expenses):
                category = random.choice(
                    Category.objects.filter(type="expense", account=family_account)
                )
                # 根据分类决定金额范围
                main_cat = category.name.split("-")[0]
                min_amount, max_amount = expense_ranges.get(
                    main_cat, (Decimal("10.00"), Decimal("200.00"))
                )
                amount = Decimal(
                    str(random.uniform(float(min_amount), float(max_amount)))
                ).quantize(Decimal("0.01"))

                # 特殊日期（节假日）消费金额翻倍
                if current_date.day == 1 or current_date.weekday() >= 5:
                    amount *= Decimal(str(random.uniform(1.2, 2.0))).quantize(
                        Decimal("0.01")
                    )

                Bill.objects.create(
                    account=family_account,
                    type="expense",
                    amount=amount,
                    category=category,
                    date=current_date + timedelta(hours=random.randint(9, 21)),
                    description=f"日常{category.name}",
                    created_by=user,
                )

        # 个人账本支出
        if random.random() < daily_expense_prob * 0.7:  # 个人支出概率稍低
            num_expenses = random.randint(1, 2)
            for _ in range(num_expenses):
                category = random.choice(
                    Category.objects.filter(type="expense", account=personal_account)
                )
                main_cat = category.name.split("-")[0]
                min_amount, max_amount = expense_ranges.get(
                    main_cat, (Decimal("5.00"), Decimal("100.00"))
                )
                # 个人支出金额较小
                amount = (
                    Decimal(str(random.uniform(float(min_amount), float(max_amount))))
                    * Decimal("0.5")
                ).quantize(Decimal("0.01"))

                Bill.objects.create(
                    account=personal_account,
                    type="expense",
                    amount=amount,
                    category=category,
                    date=current_date + timedelta(hours=random.randint(9, 21)),
                    description=f"个人{category.name}",
                    created_by=user,
                )

        # 随机收入（兼职、红包等）
        if random.random() < 0.05:  # 5%的概率有额外收入
            category = random.choice(
                Category.objects.filter(
                    name__startswith="其他", type="income", account=personal_account
                )
            )
            amount = Decimal(str(round(random.uniform(100, 1000), 2)))
            Bill.objects.create(
                account=personal_account,
                type="income",
                amount=amount,
                category=category,
                date=current_date + timedelta(hours=random.randint(9, 21)),
                description=f"额外{category.name}收入",
                created_by=user,
            )

        current_date += timedelta(days=1)

    # 6. 创建预算 - 根据实际支出设置更合理的预算
    def calculate_average_monthly_expense(category_name):
        start_of_month = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(
            days=1
        )
        three_months_ago = start_of_month - timedelta(days=90)

        total_expense = Bill.objects.filter(
            account=family_account,
            type="expense",
            category__name__startswith=category_name,
            date__gte=three_months_ago,
            date__lt=start_of_month,
        ).aggregate(models.Sum("amount"))["amount__sum"] or Decimal("0")

        return round(total_expense * Decimal("1.1"))  # 预算设为平均支出的1.1倍

    budget_categories = ["餐饮", "交通", "购物", "居住", "娱乐", "医疗", "教育"]

    current_month_start = timezone.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    current_month_end = (current_month_start + timedelta(days=32)).replace(
        day=1
    ) - timedelta(days=1)

    for main_cat in budget_categories:
        # 获取该主分类下的第一个子分类
        category = Category.objects.filter(
            name__startswith=main_cat, type="expense", account=family_account
        ).first()

        # 根据历史数据设置预算
        amount = calculate_average_monthly_expense(main_cat)

        Budget.objects.get_or_create(
            account=family_account,
            category=category,
            amount=amount,
            start_date=current_month_start,
            end_date=current_month_end,
        )


if __name__ == "__main__":
    create_test_data()
    print("测试数据创建完成！")
