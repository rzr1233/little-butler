from django.urls import path
from . import views

app_name = "bills"

urlpatterns = [
    # 账本相关
    path("accounts/", views.AccountListView.as_view(), name="account-list"),
    path("accounts/create/", views.AccountCreateView.as_view(), name="account-create"),
    path(
        "accounts/<int:pk>/", views.AccountDetailView.as_view(), name="account-detail"
    ),
    path(
        "accounts/<int:pk>/update/",
        views.AccountUpdateView.as_view(),
        name="account-update",
    ),
    path(
        "accounts/<int:pk>/delete/",
        views.AccountDeleteView.as_view(),
        name="account-delete",
    ),
    # 账单相关
    path(
        "accounts/<int:account_pk>/bills/create/",
        views.BillCreateView.as_view(),
        name="bill-create",
    ),
    path(
        "bills/<int:pk>/update/",
        views.BillUpdateView.as_view(),
        name="bill-update",
    ),
    path(
        "bills/<int:pk>/delete/",
        views.BillDeleteView.as_view(),
        name="bill-delete",
    ),
    # API endpoints
    path(
        "api/accounts/<int:account_pk>/categories/",
        views.get_account_categories,
        name="api-account-categories",
    ),
]
