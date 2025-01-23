from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "用户管理"
    path = "/home/zyn1233/little-butler/accounts"  # 显式指定路径
