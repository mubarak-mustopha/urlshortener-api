import secrets
from django.http import HttpRequest
from string import ascii_letters, digits


from .models import URL

CHARS = ascii_letters + digits


def generate_key(key_length):
    return "".join([secrets.choice(CHARS) for _ in range(key_length)])


def generate_unique_key(key_length=5):
    key = generate_key(key_length)
    if not URL.objects.filter(key=key).exists():
        return key
    return generate_unique_key(key_length)


def build_absolute_url(request: HttpRequest, path: str) -> str:
    absolute_url = "{scheme}://{domain}{path}"

    return absolute_url.format(
        scheme=request.scheme,
        domain=request.get_host(),
        path=path,
    )
