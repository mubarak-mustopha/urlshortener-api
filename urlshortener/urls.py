from django.urls import path, re_path

from .utils import KEY_PAT, SECRET_KEY_PAT
from .views import create_shortened_url, forward_target_url, get_admin_info


urlpatterns = [
    path("url/", create_shortened_url, name="create-shortened-url"),
    re_path(
        r"^(?P<key>" + KEY_PAT + r")/$",
        forward_target_url,
        name="forward-target-url",
    ),
    re_path(
        r"^(?P<secret_key>" + SECRET_KEY_PAT + r")/$",
        get_admin_info,
        name="get-admin-info",
    ),
]
