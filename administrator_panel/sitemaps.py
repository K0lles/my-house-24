from django.contrib.sitemaps import Sitemap

from .models import *


class HouseSitemap(Sitemap):

    def items(self):
        return House.objects.all()


class FlatSitemap(Sitemap):

    def items(self):
        return Flat.objects.all()


class PersonalAccountSitemap(Sitemap):

    def items(self):
        return PersonalAccount.objects.all()


class NotorietySitemap(Sitemap):

    def items(self):
        return Notoriety.objects.all()


class ReceiptSitemap(Sitemap):

    def items(self):
        return Receipt.objects.all()


class ApplicationSitemap(Sitemap):

    def items(self):
        return Application.objects.all()


class MessageSitemap(Sitemap):

    def items(self):
        return Message.objects.all()


class EvidenceSitemap(Sitemap):

    def items(self):
        return Evidence.objects.all()
