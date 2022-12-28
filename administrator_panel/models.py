from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from configuration.models import User, Tariff, ArticlePayment, Service


class House(models.Model):
    house_user = models.ManyToManyField(User, related_name='users', through='HouseUser', through_fields=('house', 'user'))
    name = models.CharField(max_length=200, verbose_name='Назва')
    address = models.CharField(max_length=200, verbose_name='Адреса')
    photo_1 = models.ImageField(upload_to='houses/photos/', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='houses/photos/', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='houses/photos/', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='houses/photos/', blank=True, null=True)
    photo_5 = models.ImageField(upload_to='houses/photos/', blank=True, null=True)


class HouseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Section(models.Model):
    house = models.ForeignKey(House, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, verbose_name='Поверх')


class Floor(models.Model):
    house = models.ForeignKey(House, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, verbose_name='Назва')


class Flat(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(0)])
    house = models.ForeignKey(House, on_delete=models.PROTECT, verbose_name='Дім')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name='Секція')
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, verbose_name='Поверх')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Власник', blank=True, null=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, verbose_name='Тариф', blank=True, null=True)
    square = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Площа')


class PersonalAccount(models.Model):
    number = models.CharField(max_length=255, verbose_name='Номер', unique=True)
    flat = models.OneToOneField(Flat, on_delete=models.SET_NULL, verbose_name='Квартира', blank=True, null=True)

    class Status(models.TextChoices):
        active = ('active', 'Активний')
        inactive = ('inactive', 'Неактивний')

    status = models.CharField(max_length=15, choices=Status.choices, default='inactive', verbose_name='Статус')


class Notoriety(models.Model):
    number = models.CharField(max_length=255, unique=True)
    account = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, verbose_name='Особовий рахунок', blank=True,
                                null=True)
    article = models.ForeignKey(ArticlePayment, on_delete=models.PROTECT, verbose_name='Стаття')
    sum = models.FloatField(verbose_name='Сума')
    comment = models.TextField(verbose_name='Коментар', blank=True, null=True)
    is_completed = models.BooleanField(default=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер', related_name='manager')    # only user with role 'manager'

    class TypeChoices(models.TextChoices):
        income = ('income', 'Прихід')
        outcome = ('outcome', 'Розхід')

    type = models.CharField(max_length=20, choices=TypeChoices.choices, default='income')    # is set in view while saving - income or outcome
    created_at = models.DateField(default=timezone.now)


class Receipt(models.Model):
    number = models.CharField(max_length=8, unique=True)
    account = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, verbose_name='Особовий рахунок')
    date_from = models.DateField(verbose_name='Період з', default=timezone.now)
    date_to = models.DateField(verbose_name='Період по', default=timezone.now)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name='Тариф', blank=True, null=True)
    is_completed = models.BooleanField(default=True)

    class StatusChoices(models.TextChoices):
        paid = ('paid', 'Оплачена')
        partly_paid = ('partly paid', 'Частково оплачена')
        not_paid = ('not paid', 'Не оплачена')

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default='paid', verbose_name='Статус')
    created_at = models.DateField(default=timezone.now)


class Application(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира')

    class MasterTypeChoices(models.TextChoices):
        all = ('', 'Будь-який спеціаліст')
        plumber = ('plumber', 'Сантехнік')
        electrician = ('electrician', 'Електрик')

    master_type = models.CharField(max_length=20, choices=MasterTypeChoices.choices, verbose_name='Тип майстра')
    master = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Майстер', blank=True, null=True)
    description = models.TextField(verbose_name='Опис')
    comment = models.TextField(blank=True, null=True)

    class StatusChoices(models.TextChoices):
        new = ('new', 'Нова')
        in_work = ('in work', 'У роботі')
        completed = ('completed', 'Виконана')

    status = models.CharField(max_length=15, choices=StatusChoices.choices, verbose_name='Статус', default='new')
    desired_date = models.DateField(default=timezone.now)
    desired_time = models.TimeField(default=timezone.now)
    created_by_director = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Відправник', related_name='sender', blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Кому', related_name='receiver', blank=True, null=True)
    theme = models.CharField(max_length=200, verbose_name='Тема')
    main_text = models.TextField(verbose_name='Повідомлення')
    created_at = models.DateTimeField(auto_now=True)


class Template(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='receipts/templates')
    is_default = models.BooleanField(default=False, verbose_name='За замовчуванням')


class Evidence(models.Model):
    number = models.CharField(max_length=15, unique=True)
    flat = models.ForeignKey(Flat, on_delete=models.PROTECT, verbose_name='Квартира')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name='Рахунок')

    class StatusChoices(models.TextChoices):
        new = ('new', 'Новий')
        null = ('null', 'Нульовий')
        taken = ('taken', 'Врахований')
        taken_and_paid = ('taken and paid', 'Врахований і оплачений')

    status = models.CharField(max_length=20, choices=StatusChoices.choices, verbose_name='Статус')
    counter_evidence = models.FloatField(validators=[MinValueValidator(0.0)])
    date_from = models.DateField(default=timezone.now)


class ReceiptService(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='receiptservices')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='service')
    amount = models.FloatField(default=0.00)
    price = models.FloatField(default=0.00)
    total_price = models.FloatField(default=0.00)
