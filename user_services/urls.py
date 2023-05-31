from django.urls import path
from user_services.views import CreateUserView, ManageUserView, CreateTokenView, LogOutView

app_name = "user_services"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("log_out/", LogOutView.as_view(), name="log_out"),
]
