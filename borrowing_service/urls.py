from django.urls import path

from borrowing_service.views import BorrowingViewSet


urlpatterns = [
    path(
        "borrowings/",
        BorrowingViewSet.as_view({"get": "list"}),
        name="borrowing_list",
    ),
    path(
        "borrowings/borrow/",
        BorrowingViewSet.as_view({"post": "borrow"}),
        name="borrow",
    ),
    path(
        "borrowings/<int:pk>/return/",
        BorrowingViewSet.as_view({"post": "return_book"}),
        name="return_book",
    ),
]


app_name = "borrowing_service"
