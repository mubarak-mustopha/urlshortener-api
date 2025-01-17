from django.urls import path

from .views import create_shortened_url, forward_target_url, get_admin_info

urlpatterns = [
    path("url/", create_shortened_url, name="create-shortened-url"),
    path("<str:key>/", forward_target_url, name="forward-target-url"),
    path("<str:secret_key>/", get_admin_info, name="get-admin-info"),
]
