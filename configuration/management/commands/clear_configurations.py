from django.core.management.base import BaseCommand

from configuration.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.all().delete()
        Role.objects.all().delete()
        Tariff.objects.all().delete()
        TariffService.objects.all().delete()
        ArticlePayment.objects.all().delete()
        PaymentRequisite.objects.all().delete()
        Service.objects.all().delete()
        MeasurementUnit.objects.all().delete()
