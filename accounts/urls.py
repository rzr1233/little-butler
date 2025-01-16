from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    # 用户认证
    path("register/", views.register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # 密码管理
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url="/accounts/password-change/done/",
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # 用户档案
    path("profile/", views.profile_view, name="profile"),
    # 家庭管理
    path("family/create/", views.FamilyCreateView.as_view(), name="family-create"),
    path("family/list/", views.FamilyListView.as_view(), name="family-list"),
    path("family/<int:pk>/", views.family_detail_view, name="family-detail"),
    # 密码重置相关URL
    path(
        "password_reset/",
        views.CustomPasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url="/accounts/password_reset/done/",
            from_email=None,  # 使用settings.py中的DEFAULT_FROM_EMAIL
            html_email_template_name=None,  # 禁用HTML邮件
            extra_email_context={"site_name": "记账软件"},  # 添加额外的上下文
            extra_context={"title": "重置密码"},  # 添加页面标题
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/accounts/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
