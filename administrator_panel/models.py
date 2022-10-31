from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from configuration.models import User, Tariff, ArticlePayment


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
    number = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    house = models.ForeignKey(House, on_delete=models.PROTECT, verbose_name='Дім')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name='Секція')
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, verbose_name='Поверх')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Власник')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, verbose_name='Тариф')
    square = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Площа')


class PersonalAccount(models.Model):
    number = models.CharField(max_length=255, verbose_name='Номер', unique=True)
    flat = models.OneToOneField(Flat, on_delete=models.CASCADE, verbose_name='Квартира', blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='Статус')


class Notoriety(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Власник', related_name='owner', blank=True,
                              null=True)
    account = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, verbose_name='Особовий рахунок', blank=True,
                                null=True)
    article = models.ForeignKey(ArticlePayment, on_delete=models.CASCADE, verbose_name='Стаття')
    sum = models.FloatField(validators=[MinValueValidator(0.0)], verbose_name='Сума')
    comment = models.TextField(verbose_name='Коментар')
    is_completed = models.BooleanField(default=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер', related_name='manager')    # only user with role 'manager'

    class TypeChoices(models.TextChoices):
        income = 'income'
        outcome = 'outcome'

    type = models.CharField(max_length=20, choices=TypeChoices.choices, default='income')    # is set in view while saving - income or outcome
    created_at = models.DateTimeField(default=timezone.now)


class Receipt(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Власник')
    account = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, verbose_name='Особовий рахунок')
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='Дім')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name='Секція')
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name='Тариф')
    is_completed = models.BooleanField(default=False)

    class StatusChoices(models.TextChoices):
        paid = ('paid', 'Оплачена')
        partly_paid = ('partly paid', 'Частково оплачена')
        not_paid = ('not paid', 'Не оплачена')

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default='paid', verbose_name='Статус')
    phone = PhoneNumberField(verbose_name='Номер телефону')
    created_at = models.DateTimeField(default=timezone.now)


class Application(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Власник')
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира')

    class MasterTypeChoices(models.TextChoices):
        all = ('', 'Будь-який')
        plumber = ('plumber', 'Сантехнік')
        electrician = ('electrician', 'Електрик')

    master_type = models.CharField(max_length=20, choices=MasterTypeChoices.choices, verbose_name='Тип майстра')
    description = models.TextField(verbose_name='Опис')

    class StatusChoices(models.TextChoices):
        new = ('new', 'Нова')
        in_work = ('in work', 'У роботі')
        completed = ('completed', 'Виконана')

    status = models.CharField(max_length=15, choices=StatusChoices.choices, verbose_name='Статус')
    created_at = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Відправник', related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Кому', related_name='receiver')
    theme = models.CharField(max_length=200, verbose_name='Тема')
    main_text = models.TextField(verbose_name='Повідомлення')
    is_read = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)


class Template(models.Model):
    file = models.FileField(upload_to='receipts/templates')
    is_default = models.BooleanField(default=False, verbose_name='За замовчуванням')


class Evidence(models.Model):
    house = models.ForeignKey(House, on_delete=models.PROTECT, verbose_name='Дім')
    flat = models.ForeignKey(Flat, on_delete=models.PROTECT, verbose_name='Квартира')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name='Секція')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, verbose_name='Рахунок')

    class StatusChoices(models.TextChoices):
        new = ('new', 'Новий')
        null = ('null', 'Нульовий')
        taken = ('taken', 'Врахований')

    status = models.CharField(max_length=10, choices=StatusChoices.choices, verbose_name='Статус')
    counter_evidence = models.FloatField(validators=[MinValueValidator(0.0)])
