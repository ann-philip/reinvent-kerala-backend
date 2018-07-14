from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator


class Role(models.Model):
    name = models.CharField(max_length=20)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    phone_number_validator = RegexValidator(regex=r'^\+?1?\d{5,13}$')
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150, unique=True, validators=[username_validator])
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(
        max_length=15, validators=[phone_number_validator],  blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField(Role)
    tags = models.ManyToManyField(Tag)
    github_username = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @property
    def full_name(self):
        self.get_full_name()
