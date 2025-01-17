from django.db import models

from django.urls import reverse

# Create your models here.


class URL(models.Model):

    target_url = models.URLField()
    key = models.CharField(unique=True, max_length=50)
    secret_key = models.CharField(unique=True, max_length=50)
    clicks = models.PositiveIntegerField(default=0)

    # use to control deletion of urls
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.target_url

    def get_absolute_url(self):
        return reverse("forward-target-url", kwargs={"key": self.key})

    @property
    def shortened_url_path(self):
        return self.get_absolute_url()

    @property
    def admin_url_path(self):
        return f"/admin/{self.secret_key}/"
