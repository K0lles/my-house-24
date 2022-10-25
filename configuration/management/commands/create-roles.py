from django.core.management.base import BaseCommand

from configuration.models import Role


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Role.objects.all().exists():

            Role.objects.create(role='director',
                                statistic_access=True,
                                checkout_access=True,
                                receipt_access=True,
                                bill_access=True,
                                flat_access=True,
                                owner_access=True,
                                building_access=True,
                                message_access=True,
                                master_apply_access=True,
                                counter_access=True,
                                site_management_access=True,
                                service_access=True,
                                tariff_access=True,
                                role_access=True,
                                user_access=True,
                                payment_requisite_access=True)

            Role.objects.create(role='user')
            Role.objects.create(role='manager',
                                statistic_access=True,
                                checkout_access=True,
                                receipt_access=True,
                                bill_access=True,
                                flat_access=True,
                                owner_access=True,
                                building_access=True,
                                message_access=True,
                                master_apply_access=True,
                                counter_access=True,
                                site_management_access=True,
                                service_access=True,
                                tariff_access=True,
                                role_access=True,
                                user_access=True,
                                payment_requisite_access=True)

            Role.objects.create(role='accountant',
                                statistic_access=True,
                                checkout_access=True,
                                receipt_access=True,
                                bill_access=True,
                                flat_access=True,
                                owner_access=True,
                                building_access=True,
                                message_access=True,
                                master_apply_access=True,
                                counter_access=True,
                                tariff_access=True,
                                payment_requisite_access=True)

            Role.objects.create(role='electrician',
                                message_access=True,
                                flat_access=True,
                                building_access=True,
                                counter_access=True,
                                master_apply_access=True)

            Role.objects.create(role='plumber',
                                message_access=True,
                                flat_access=True,
                                building_access=True,
                                counter_access=True,
                                master_apply_access=True)
            Role.objects.create(role='owner')
