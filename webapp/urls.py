from django.urls import path

from webapp.views import AccountListView, CSVUploadView

urlpatterns = [
    path("accounts/", AccountListView.as_view(), name="account-list"),
    path("upload/", CSVUploadView.as_view(), name="upload"),
]
