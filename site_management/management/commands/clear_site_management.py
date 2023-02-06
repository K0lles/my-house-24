from django.core.management.base import BaseCommand

from site_management.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        MainPage.objects.all().delete()
        AboutUs.objects.all().delete()
        ServiceFront.objects.all().delete()
        TariffPage.objects.all().delete()
        Contact.objects.all().delete()

        ServiceObjectFront.objects.all().delete()
        TariffObjectFront.objects.all().delete()
        Document.objects.all().delete()
        Seo.objects.all().delete()
        Gallery.objects.all().delete()
