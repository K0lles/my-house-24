from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField


class Role(models.Model):
    class RoleChoices(models.TextChoices):
        director = ('director', 'Директор')
        user = ('user', 'Користувач')
        manager = ('manager', 'Менеджер')
        accountant = ('accountant', 'Бухгалтер')
        electrician = ('electrician', 'Електрик')
        plumber = ('plumber', 'Сантехнік')
        owner = ('owner', 'Власник')

    role = models.CharField(max_length=40, choices=RoleChoices.choices, default='user')

    statistic_access = models.BooleanField(default=False)
    checkout_access = models.BooleanField(default=False)
    receipt_access = models.BooleanField(default=False)
    bill_access = models.BooleanField(default=False)
    flat_access = models.BooleanField(default=False)
    owner_access = models.BooleanField(default=False)
    building_access = models.BooleanField(default=False)
    message_access = models.BooleanField(default=False)
    master_apply_access = models.BooleanField(default=False)
    counter_access = models.BooleanField(default=False)
    site_management_access = models.BooleanField(default=False)
    service_access = models.BooleanField(default=False)
    tariff_access = models.BooleanField(default=False)
    role_access = models.BooleanField(default=False)
    user_access = models.BooleanField(default=False)
    payment_requisite_access = models.BooleanField(default=False)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', unique=True)
    name = models.CharField(max_length=200, verbose_name="Ім'я")
    surname = models.CharField(max_length=200, verbose_name='Прізвище')
    birthday = models.DateField(verbose_name='Дата народження', blank=True, null=True)
    logo = models.ImageField(upload_to='users/logos/', verbose_name='Лого', blank=True, null=True)
    father = models.CharField(max_length=200, verbose_name='По батькові', blank=True, null=True)
    phone = PhoneNumberField(verbose_name='Номер телефону', blank=True, null=True)
    viber = models.CharField(max_length=200, verbose_name='Viber', blank=True, null=True)
    owner_id = models.CharField(max_length=55, verbose_name='ID', blank=True, null=True)
    telegram = models.CharField(max_length=200, verbose_name='Telegram', blank=True, null=True)

    class StatusChoices(models.TextChoices):
        new = ('new', 'Новий')
        active = ('active', 'Активний')
        disconnected = ('disconnected', 'Відключений')

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default='new', verbose_name='Статус')
    notes = models.TextField(verbose_name='Нотатки', blank=True, null=True)
    password = models.CharField(max_length=200, verbose_name='Пароль')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name='Роль')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class MeasurementUnit(models.Model):
    name = models.CharField(max_length=200, verbose_name='Од. вим.')
    is_used = models.BooleanField(default=False)


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва послуги')
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.PROTECT)
    show_in_counters = models.BooleanField(default=True, verbose_name='Показувати в рахунок')
    is_used = models.BooleanField(default=False)


class Tariff(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва тарифу')
    description = models.TextField(verbose_name='Опис тарифу')
    service_tariff = models.ManyToManyField(Service, through='TariffService', through_fields=('tariff', 'service'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редагування')


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Послуга')
    price = models.FloatField(verbose_name='Ціна', validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=55, verbose_name='Валюта', default='грн')

    def delete(self, using=None, keep_parents=False):
        if not self.service.tariffservice_set.all().exists() \
                or (self.service.tariffservice_set.all().count() == 1 and self.service.tariffservice_set.all()[0].pk == self.pk):
            self.service.is_used = False
            self.service.save()
        return super(TariffService, self).delete(using, keep_parents)


class ArticlePayment(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')

    class TypeChoices(models.TextChoices):
        income = ('income', 'Прихід')
        outcome = ('outcome', 'Розхід')

    type = models.CharField(max_length=10, choices=TypeChoices.choices, verbose_name='Прихід/Розхід')


class PaymentRequisite(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва компанії')
    information = models.TextField(verbose_name='Інформація')
