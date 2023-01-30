import random

from django.core.management.base import BaseCommand
from faker import Faker

from configuration.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Tariff.objects.all().count() == 0 and MeasurementUnit.objects.all().count() == 0 \
                and Service.objects.all().count() == 0:
            kv_per_hour = MeasurementUnit.objects.create(
                name='кВт*год',
                is_used=True
            )

            m2 = MeasurementUnit.objects.create(
                name='м2',
                is_used=True
            )

            m3 = MeasurementUnit.objects.create(
                name='м3',
                is_used=True
            )

            m2_m3 = MeasurementUnit.objects.create(
                name='м2*м3',
                is_used=True
            )

            water = Service.objects.create(
                name='Вода',
                measurement_unit=m3,
                show_in_counters=True,
                is_used=True
            )

            light = Service.objects.create(
                name='Світло',
                measurement_unit=kv_per_hour,
                show_in_counters=True,
                is_used=True
            )

            heat = Service.objects.create(
                name='Тепло',
                measurement_unit=m2_m3,
                show_in_counters=True,
                is_used=True
            )

            gas = Service.objects.create(
                name='Газ',
                measurement_unit=m3,
                show_in_counters=True,
                is_used=True
            )

            area_guard = Service.objects.create(
                name='Охорона території',
                measurement_unit=m2,
                show_in_counters=True,
                is_used=True
            )

            base_tariff = Tariff.objects.create(
                name='Базовий тариф',
                description='Базовий тариф, який надає користувачам звичайні блага цивілізації.',
            )

            TariffService.objects.create(
                tariff=base_tariff,
                service=water,
                price=3.12,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=base_tariff,
                service=light,
                price=1.6,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=base_tariff,
                service=heat,
                price=2.64,
                currency='грн'
            )

            discount_tariff = Tariff.objects.create(
                name='Дисконтний тариф',
                description='Тариф зі зниженими цінами для особливих клієнтів',
            )

            TariffService.objects.create(
                tariff=discount_tariff,
                service=water,
                price=2.8,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=discount_tariff,
                service=light,
                price=1.4,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=discount_tariff,
                service=heat,
                price=2.2,
                currency='грн'
            )

            gas_heat_tariff = Tariff.objects.create(
                name='Тариф з отопленням газом',
                description='Тариф, в який включено отоплення газом',
            )

            TariffService.objects.create(
                tariff=gas_heat_tariff,
                service=water,
                price=2.8,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=gas_heat_tariff,
                service=light,
                price=1.4,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=gas_heat_tariff,
                service=gas,
                price=4.7,
                currency='грн'
            )

            elite_tariff = Tariff.objects.create(
                name='Елітний тариф',
                description='LUX умови тарифу із охороною території'
            )

            TariffService.objects.create(
                tariff=elite_tariff,
                service=area_guard,
                price=25.2,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=elite_tariff,
                service=water,
                price=2.8,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=elite_tariff,
                service=light,
                price=1.4,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=elite_tariff,
                service=gas,
                price=4.7,
                currency='грн'
            )

            TariffService.objects.create(
                tariff=elite_tariff,
                service=heat,
                price=2.2,
                currency='грн'
            )

        if ArticlePayment.objects.all().count() == 0:
            ArticlePayment.objects.create(
                name='Прихід на рахунок',
                type='income'
            )

            ArticlePayment.objects.create(
                name='Прихід згідно оплати',
                type='income'
            )

            ArticlePayment.objects.create(
                name='Розхід із картки',
                type='outcome'
            )

        if PaymentRequisite.objects.all().count() == 0:
            PaymentRequisite.objects.create(
                name='Платіжні реквізити Мой Дом 24',
                information='Інформація про платіжний реквізит Мой Дом 24'
            )

        if User.objects.all().exclude(role__role='owner').count() == 0 \
                and Role.objects.all().exists():
            fake = Faker('uk_UA')
            User.objects.create_user(
                email='superuser@gmail.com',
                password='123qweasd',
                name='Головний',
                surname='Адміністратор',
                phone='+380990000000',
                status='active',
                is_active=True,
                role=Role.objects.get(role='director')
            )

            for i in range(0, 7):
                User.objects.create_user(
                    email=fake.ascii_email(),
                    password='123qweasd',
                    name=fake.first_name(),
                    surname=fake.last_name(),
                    phone=fake.phone_number(),
                    status='active',
                    is_active=True,
                    role=Role.objects.get(role=random.choice(['plumber', 'manager', 'accountant', 'electrician']))
                )
