from django.core.management.base import BaseCommand

from administrator_panel.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        Application.objects.all().delete()
        Evidence.objects.all().delete()
        Notoriety.objects.all().delete()
        ReceiptService.objects.all().delete()
        Receipt.objects.all().delete()
        PersonalAccount.objects.all().delete()
        Flat.objects.all().delete()
        Floor.objects.all().delete()
        Section.objects.all().delete()
        House.objects.all().delete()
