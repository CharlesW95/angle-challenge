from django.urls import include, path

urlpatterns = [
    path("api/", include("angle_store_backend.urls"))
]
