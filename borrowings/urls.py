from django.urls import path

from borrowings.views import BorrowingViewSet


urlpatterns = [
    path(
        "",
        BorrowingViewSet.as_view({"get": "list"}),
        name="borrowing_list",
    ),
    path(
        "<int:pk>/",
        BorrowingViewSet.as_view({"get": "retrieve"}),
        name="borrowing_detail",
    ),
    path(
        "borrow/",
        BorrowingViewSet.as_view({"post": "borrow"}),
        name="borrow",
    ),
    path(
        "<int:pk>/return/",
        BorrowingViewSet.as_view({"post": "return_book"}),
        name="return_book",
    ),
]


app_name = "borrowings"
