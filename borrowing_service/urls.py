from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from borrowing_service.views import BorrowingViewSet

router = DefaultRouter()
router.register("borrowings", BorrowingViewSet, basename="borrowings")

app_name = "borrowing_service"

urlpatterns = [
    path("", include(router.urls)),
]
