import datetime
import random
from string import digits

from django.core.management.base import BaseCommand
from faker import Faker

from administrator_panel.models import *
from configuration.models import Role, TariffService


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker('uk_UA')

        if House.objects.all().count() < 100:
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
                sections_number = Section.objects.filter(house=house).count()
                for i in range(1, random.randint(4, 6)):
                    Section.objects.create(
                        house=house,
                        name=f'Секція {sections_number + i}'
                    )

                floors_number = Floor.objects.filter(house=house).count()
                for i in range(1, random.randint(4, 6)):
                    Floor.objects.create(
                        house=house,
                        name=f'Поверх {floors_number + i}'
                    )

        if not User.objects.filter(role__role='owner').count() < 35:
            for i in range(0, random.randint(7, 10)):
                User.objects.create_user(
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

        if Flat.objects.all().count() < 40:

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

        if Receipt.objects.all().count() < 145:
            for i in range(0, 29):
                flat = random.choice(Flat.objects
                                     .select_related('personalaccount',
                                                     'tariff')
                                     .prefetch_related('tariff__service_tariff__service')
                                     .filter(personalaccount__isnull=False))
                date_from = fake.date_between(datetime.datetime(datetime.datetime.now().year - 1,
                                                                datetime.datetime.now().month,
                                                                datetime.datetime.now().day),
                                              datetime.datetime.now())

                if date_from.month != 12:
                    try:
                        date_to = datetime.datetime(date_from.year, date_from.month + 1, date_from.day)
                    except ValueError:
                        date_to = datetime.datetime(date_from.year, date_from.month + 1, 28)
                else:
                    date_to = datetime.datetime(date_from.year + 1, 1, date_from.day)

                receipt = Receipt.objects.create(
                    number=''.join(random.choice(digits) for i in range(8)),
                    account=flat.personalaccount,
                    date_from=date_from,
                    date_to=date_to,
                    tariff=flat.tariff,
                    is_completed=True,
                    status=random.choice(['paid', 'partly paid', 'not paid']),
                    created_at=date_from
                )

                for z in range(0, random.randint(3, 7)):
                    service = random.choice(Service.objects.filter(tariff=flat.tariff))
                    try:
                        tariff_service_price = TariffService.objects.get(tariff=flat.tariff, service=service).price
                    except TariffService.DoesNotExist:
                        tariff_service_price = format(random.uniform(0.10, 10.85), ".2f")
                    amount = format(random.uniform(1.10, 250.35), ".2f")
                    ReceiptService.objects.create(
                        receipt=receipt,
                        service=service,
                        amount=amount,
                        price=tariff_service_price,
                        total_price=format(float(amount) * tariff_service_price, ".2f")
                    )

        if Notoriety.objects.filter(type='income').count() < 50:
            for i in range(0, random.randint(7, 14)):
                account = random.choice(PersonalAccount.objects.filter(flat__isnull=False))
                Notoriety.objects.create(
                    number=''.join(random.choice(digits) for i in range(8)),
                    account=account,
                    article=random.choice(ArticlePayment.objects.filter(type='income')),
                    sum=random.randint(260, 14890),
                    is_completed=True,
                    manager=random.choice(User.objects.filter(role__role='manager')),
                    type='income',
                    created_at=fake.date_between(datetime.datetime(datetime.datetime.now().year - 1,
                                                                datetime.datetime.now().month,
                                                                datetime.datetime.now().day),
                                                 datetime.datetime.now())
                )

        if Notoriety.objects.filter(type='outcome').count() < 30:
            for i in range(0, random.randint(10, 14)):
                Notoriety.objects.create(
                    number=''.join(random.choice(digits) for i in range(8)),
                    article=random.choice(ArticlePayment.objects.filter(type='outcome')),
                    sum=random.randint(450, 6900),
                    is_completed=True,
                    manager=random.choice(User.objects.filter(role__role='manager')),
                    type='outcome',
                    created_at=fake.date_between(datetime.datetime(datetime.datetime.now().year - 1,
                                                                datetime.datetime.now().month,
                                                                datetime.datetime.now().day),
                                                 datetime.datetime.now())
                )

        if Evidence.objects.all().count() < 70:
            for i in range(0, random.randint(16, 22)):
                flat = random.choice(Flat.objects.filter(personalaccount__isnull=False))
                service = random.choice(Service.objects.filter(tariff=flat.tariff))
                Evidence.objects.create(
                    number=''.join(random.choice(digits) for i in range(8)),
                    flat=flat,
                    service=service,
                    status=random.choice(['new', 'null', 'taken', 'taken and paid']),
                    counter_evidence=format(random.uniform(29.0, 689.20), ".2f"),
                    date_from=fake.date_between(datetime.datetime(datetime.datetime.now().year - 1,
                                                                datetime.datetime.now().month,
                                                                datetime.datetime.now().day),
                                                datetime.datetime.now())
                )

        if Application.objects.all().count() < 25:
            for i in range(0, 5):
                flat = random.choice(Flat.objects.filter(personalaccount__isnull=False))
                master = random.choice(User.objects.filter(role__role__in=['plumber', 'electrician']))
                Application.objects.create(
                    flat=flat,
                    master_type=master.role.role,
                    master=master,
                    description=fake.paragraph(nb_sentences=5),
                    status=random.choice(['new', 'in work', 'completed']),
                    created_by_director=True,
                    desired_date=fake.date_time_between(datetime.datetime(datetime.datetime.now().year - 1,
                                                                datetime.datetime.now().month,
                                                                datetime.datetime.now().day),
                                              datetime.datetime.now()),
                    desired_time=fake.date_time_between_dates(datetime.datetime(datetime.datetime.now().year - 1,
                                                                datetime.datetime.now().month,
                                                                datetime.datetime.now().day),
                                                    datetime.datetime.now())
                )

        if not Template.objects.all().exists():
            Template.objects.create(
                name='Шаблон',
                file='start_commands/template/template-first.xlsx',
                is_default=True
            )
