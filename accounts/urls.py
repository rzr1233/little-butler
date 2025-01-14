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
]
