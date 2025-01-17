from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import URL
from .serializers import URLSerializer
from .utils import build_absolute_url


# Create your views here.
@extend_schema(
    request=URLSerializer,
    responses={201: URLSerializer},
    summary="Create shortened url",
    description="Create shortened url",
)
@api_view(http_method_names=["POST"])
def create_shortened_url(request):
    serializer = URLSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()

    data = serializer.data
    data["url"] = build_absolute_url(request, path=data["url"])
    data["admin_url"] = build_absolute_url(request, path=data["admin_url"])

    return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Foward shortened url to target url",
)
@api_view(
    http_method_names=["GET"],
)
def forward_target_url(request, key) -> HttpResponseRedirect:
    # http://127.0.0.1:8000/Yfs62
    url: URL = get_object_or_404(URL, key=key)
    return HttpResponseRedirect(url.target_url)


@extend_schema(
    responses={204: None},
    methods=["DELETE"],
    description="Delete url data by providing secret key",
)
@extend_schema(
    responses={200: URLSerializer},
    methods=["GET"],
    description="Get url information by providing secret key",
)
@api_view(http_method_names=["GET", "DELETE"])
def get_admin_info(request, secret_key):
    url: URL = get_object_or_404(URL, secret_key=secret_key)

    if request.method == "DELETE":
        url.is_active = False
        url.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    data = URLSerializer(url).data
    data["url"] = build_absolute_url(request, path=data["url"])
    data["admin_url"] = build_absolute_url(request, path=data["admin_url"])

    return Response(data, status=status.HTTP_200_OK)
