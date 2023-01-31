import datetime
import random
from string import digits

from django.core.management.base import BaseCommand
from faker import Faker

from administrator_panel.models import *
from configuration.models import Role, TariffService


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker()

        for i in range(0, 4):
            House.objects.create(
                name=fake.company(),
                address=fake.address()
            )

        for house in House.objects.prefetch_related('houseuser_set').all():
            user_for_house = random.choice(User.objects.filter(role__role__in=['plumber', 'manager', 'accountant', 'electrician']))
            HouseUser.objects.create(
                house=house,
                user=user_for_house
            )
            for i in range(1, random.randint(4, 6)):
                Section.objects.create(
                    house=house,
                    name=f'Секція {i}'
                )

            for i in range(1, random.randint(4, 6)):
                Floor.objects.create(
                    house=house,
                    name=f'Поверх {i}'
                )

        for i in range(0, random.randint(7, 10)):
            User.objects.create(
                email=fake.ascii_email(),
                password='123qweasd',
                name=fake.first_name(),
                surname=fake.last_name(),
                phone=fake.phone_number(),
                status='active',
                is_active=True,
                role=Role.objects.get(role='owner'),
                owner_id=''.join(random.choice(digits) for i in range(8))
            )

        for i in range(0, 9):
            house = random.choice(House.objects.prefetch_related('floor_set', 'section_set').all())
            flat = Flat.objects.create(
                number=''.join(random.choice(digits) for i in range(8)),
                house=house,
                section=random.choice(house.section_set.all()),
                floor=random.choice(house.floor_set.all()),
                owner=random.choice(User.objects.filter(role__role='owner')),
                tariff=random.choice(Tariff.objects.all()),
                square=random.randint(65, 240),
            )

            PersonalAccount.objects.create(
                number=''.join(random.choice(digits) for i in range(8)),
                flat=flat,
                status='active',
            )

        for i in range(0, 7):
            flat = random.choice(Flat.objects
                                 .select_related('personalaccount',
                                                 'tariff')
                                 .prefetch_related('tariff__service_tariff__service')
                                 .filter(personalaccount__isnull=False))
            receipt = Receipt.objects.create(
                number=''.join(random.choice(digits) for i in range(8)),
                account=flat.personalaccount,
                date_from=datetime.datetime.now(),
                date_to=datetime.datetime.date(datetime.datetime.year, datetime.datetime.month + 1, datetime.datetime.day),
                tariff=flat.tariff,
                is_completed=True,
                status=random.choice(['paid', 'partly paid', 'not paid']),
            )

            for z in range(0, random.randint(2, 7)):
                service = random.choice(Service.objects.filter(tariff=flat.tariff))
                try:
                    tariff_service_price = TariffService.objects.get(tariff=flat.tariff, service=service)
                except TariffService.DoesNotExist:
                    tariff_service_price = random.uniform(0.10, 10.85)
                amount = random.uniform(1.10, 250.35)
                ReceiptService.objects.create(
                    receipt=receipt,
                    service=service,
                    amount=amount,
                    price=tariff_service_price,
                    total_price=amount * tariff_service_price
                )

        for i in range(0, random.randint(7, 14)):
            account = random.choice(PersonalAccount.objects.filter(flat__isnull=False))
            Notoriety.objects.create(
                number=''.join(random.choice(digits) for i in range(8)),
                account=account,
                article=ArticlePayment.objects.filter(type='income'),
                sum=random.randint(260, 14890),
                is_completed=True,
                manager=random.choice(User.objects.filter(role__role='manager')),
                type='income'
            )

        for i in range(0, random.randint(4, 8)):
            Notoriety.objects.create(
                number=''.join(random.choice(digits) for i in range(8)),
                article=ArticlePayment.objects.filter(type='outcome'),
                sum=random.randint(450, 6900),
                is_completed=True,
                manager=random.choice(User.objects.filter(role__role='manager')),
                type='outcome'
            )

        for i in range(0, random.randint(12, 18)):
            flat = random.choice(Flat.objects.filter(personalaccount__isnull=False))
            service = random.choice(Service.objects.filter(tariff=flat.tariff))
            Evidence.objects.create(
                number=''.join(random.choice(digits) for i in range(8)),
                flat=flat,
                service=service,
                status=random.choice(['new', 'null', 'taken', 'taken and paid']),
                counter_evidence=random.uniform(29.0, 689.20)
            )

        for i in range(0, 5):
            flat = random.choice(Flat.objects.filter(personalaccount__isnull=False))
            master = random.choice(User.objects.filter(role__role__in=['plumber', 'accountant', 'electrician']))
            Application.objects.create(
                flat=flat,
                master_type=master.role.role,
                master=master,
                description=fake.paragraph(nb_sentences=5),
                status=random.choice(['new', 'in work', 'completed']),
                created_by_director=True
            )
