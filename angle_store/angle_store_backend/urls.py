from django.urls import path

from angle_store_backend.views import ProductCreateView, ProductSearchListView

urlpatterns = [
    path("post/", ProductCreateView.as_view()),
    path("search/", ProductSearchListView.as_view()),
]
