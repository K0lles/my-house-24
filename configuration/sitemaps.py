from django.contrib.sitemaps import Sitemap

from .models import *


class UserSitemap(Sitemap):

    def items(self):
        return User.objects.all()


class MeasurementUnitSitemap(Sitemap):

    def items(self):
        return [MeasurementUnit.objects.first()]


class ServiceObjectsSitemap(Sitemap):

    def items(self):
        return [Service.objects.first()]


class TariffSitemap(Sitemap):

    def items(self):
        return Tariff.objects.all()


class ArticlePaymentSitemap(Sitemap):

    def items(self):
        return ArticlePayment.objects.all()


class PaymentRequisiteSitemap(Sitemap):

    def items(self):
        return PaymentRequisite.objects.all()
