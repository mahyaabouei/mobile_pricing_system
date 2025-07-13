from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='کاربر')

    uniqidentifier = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='کدملی')

    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام')

    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام خانوادگی')

    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ایمیل')

    mobile = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='تلفن')

    address = models.TextField(
        null=True,
        blank=True,
        verbose_name='آدرس')

    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شهر')

    company = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام شرکت')

    sheba_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شماره شبا')

    card_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شماره کارت')

    account_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شماره حساب')

    account_bank = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام بانک')

    is_verified = models.BooleanField(
        default=False,
        verbose_name='احراز هویت شده')

    admin = models.BooleanField(
        default=False,
        verbose_name='ادمین')

    work_guarantee = models.BooleanField(
        default=False,
        verbose_name='ضمانت نامه حسن انجام کار')

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال')

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.username}"


class Otp(models.Model):
    mobile = models.CharField(max_length=255)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mobile} - {self.otp}"