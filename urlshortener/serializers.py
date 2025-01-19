from django.conf import settings
from rest_framework import serializers

from .models import URL
from .utils import generate_key, generate_unique_key


class URLSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)
    admin_url = serializers.URLField(read_only=True)

    class Meta:
        model = URL
        fields = [
            "target_url",
            "clicks",
            "is_active",
            "url",
            "admin_url",
        ]
        read_only_fields = [
            "clicks",
            "is_active",
        ]

    @property
    def data(self):
        data = super().data
        # import pdb
        # pdb.set_trace()
        if instance := self.instance:
            data["url"] = instance.shortened_url_path
            data["admin_url"] = instance.admin_url_path
        return data

    def save(self, **kwargs):
        target_url = self.validated_data["target_url"]
        key = generate_unique_key(settings.URL_KEY_LENGTH)
        secret_key = f"{key}_{generate_key(settings.URL_SECRET_KEY_LENGTH)}"

        self.instance = URL.objects.create(
            target_url=target_url, key=key, secret_key=secret_key
        )

        return self.instance
