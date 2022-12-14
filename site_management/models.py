from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from additional.models import Seo, Gallery


class MainPage(models.Model):
    seo = models.ForeignKey(Seo, on_delete=models.SET_NULL, blank=True, null=True)
    show_urls = models.BooleanField(default=True, verbose_name='Показувати посилання на додатки')
    slide_1 = models.ImageField(upload_to='main-page/slide-photos/')
    slide_2 = models.ImageField(upload_to='main-page/slide-photos/')
    slide_3 = models.ImageField(upload_to='main-page/slide-photos/')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    short_text = models.TextField(verbose_name='Короткий текст')
    block_header_1 = models.CharField(max_length=200, verbose_name='Заголовок')
    block_description_1 = models.TextField(verbose_name='Опис')
    block_photo_1 = models.ImageField(upload_to='main-page/block-photos/')
    block_header_2 = models.CharField(max_length=200, verbose_name='Заголовок')
    block_description_2 = models.TextField(verbose_name='Опис')
    block_photo_2 = models.ImageField(upload_to='main-page/block-photos/')
    block_header_3 = models.CharField(max_length=200, verbose_name='Заголовок')
    block_description_3 = models.TextField(verbose_name='Опис')
    block_photo_3 = models.ImageField(upload_to='main-page/block-photos/')
    block_header_4 = models.CharField(max_length=200, verbose_name='Заголовок')
    block_description_4 = models.TextField(verbose_name='Опис')
    block_photo_4 = models.ImageField(upload_to='main-page/block-photos/')
    block_header_5 = models.CharField(max_length=200, verbose_name='Заголовок')
    block_description_5 = models.TextField(verbose_name='Опис')
    block_photo_5 = models.ImageField(upload_to='main-page/block-photos/')
    block_header_6 = models.CharField(max_length=200, verbose_name='Заголовок')
    block_description_6 = models.TextField(verbose_name='Опис')
    block_photo_6 = models.ImageField(upload_to='main-page/block-photos/')


class AboutUs(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, blank=True, null=True)
    seo = models.ForeignKey(Seo, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    short_text = models.TextField(verbose_name='Короткий текст')
    additional_title = models.CharField(max_length=200, verbose_name='Заголовок')
    additional_text = models.TextField(verbose_name='Короткий текст')


class ServiceFront(models.Model):
    seo = models.ForeignKey(Seo, on_delete=models.SET_NULL, blank=True, null=True)
    service_photo_1 = models.ImageField(upload_to='service/photos/')
    service_title_1 = models.CharField(max_length=200, verbose_name='Назва послуги')
    service_text_1 = models.TextField(verbose_name='Опис послуги')
    service_photo_2 = models.ImageField(upload_to='service/photos/')
    service_title_2 = models.CharField(max_length=200, verbose_name='Назва послуги')
    service_text_2 = models.TextField(verbose_name='Опис послуги')
    service_photo_3 = models.ImageField(upload_to='service/photos/')
    service_title_3 = models.CharField(max_length=200, verbose_name='Назва послуги')
    service_text_3 = models.TextField(verbose_name='Опис послуги')
    service_photo_4 = models.ImageField(upload_to='service/photos/')
    service_title_4 = models.CharField(max_length=200, verbose_name='Назва послуги')
    service_text_4 = models.TextField(verbose_name='Опис послуги')


class Contact(models.Model):
    seo = models.ForeignKey(Seo, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Короткий текст')
    commercial_url = models.URLField(verbose_name='Посилання на комерційний сайт')
    name_surname_father = models.CharField(max_length=200, verbose_name='ПІБ')
    location = models.CharField(max_length=200, verbose_name='Локація')
    address = models.CharField(max_length=200, verbose_name='Адреса')
    phone = PhoneNumberField(verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    map_code = models.TextField(verbose_name='Код карти')


class Document(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE)
    file = models.FileField(upload_to='about-us/files/')
