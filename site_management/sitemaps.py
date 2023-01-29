from django.contrib.sitemaps import Sitemap

from .models import MainPage, AboutUs, ServiceFront, Contact


class MainPageSitemap(Sitemap):

    def items(self):
        return MainPage.objects.all()


class AboutUpsSitemap(Sitemap):

    def items(self):
        return AboutUs.objects.all()


class ServiceSitemap(Sitemap):

    def items(self):
        return ServiceFront.objects.all()


class ContactSitemap(Sitemap):

    def items(self):
        return Contact.objects.all()
