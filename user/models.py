from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .manager import UserManager


def image_upload_path(instance, filename):
    t = datetime.now()
    return (
        f"profilePhoto/{instance.username}/{t.day}_{t.hour}_{t.minute}_{t.microsecond}"
    )


# Create your models here.
class UserModel(AbstractUser):
    id = models.BigAutoField(unique=True, primary_key=True)
    username = models.CharField(
        unique=True,
        max_length=30,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "username"
    profilePhoto = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    location = models.CharField(null=True, max_length=30)

    class Meta:
        verbose_name = _("user")

    def __str__(self):
        return self.email
