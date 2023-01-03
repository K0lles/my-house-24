from django.db.models import Sum, Case, When, Value, FloatField, OuterRef, Subquery, Q, QuerySet

from administrator_panel.models import Flat, Notoriety


def calculate_notoriety_and_receipt_sum(personal_accounts: QuerySet):
    """Calculate incomes notoriety's sum and receipt's services sum for each personal account"""

    # making annotation separately in order to avoid multiplied wrong answer
    accounts_with_notoriety_sum = personal_accounts \
        .annotate(rest=Sum(Case(When(notoriety__sum__isnull=True, then=Value(0.00)),
                                default='notoriety__sum',
                                output_field=FloatField()))) \
        .order_by('-id')  # get sum of all notorieties bounded to account number
    accounts_with_receipt_sum = personal_accounts \
        .annotate(receipt_sum=Sum(Case(When(receipt__receiptservices__total_price__isnull=True, then=Value(0.00)),
                                       default='receipt__receiptservices__total_price',
                                       output_field=FloatField()),
                                  filter=(Q(receipt__is_completed=True)))) \
        .order_by('-id')  # get sum of all receipts bounded to account number

    # pass all annotation calculations to main object_list
    personal_accounts = personal_accounts.annotate(
        rest=Subquery(accounts_with_notoriety_sum.filter(pk=OuterRef('id')).values('rest')[:1]),
        receipt_sum=Subquery(accounts_with_receipt_sum.filter(pk=OuterRef('id')).values('receipt_sum')[:1]),
        subtraction=Case(When(rest__isnull=True, then=Value(0.00)), default='rest', output_field=FloatField()) -
                    Case(When(receipt_sum__isnull=True, then=Value(0.00)), default='receipt_sum',
                         output_field=FloatField()))

    return {'personal_accounts': personal_accounts}


def calculate_totals(personal_accounts: QuerySet):
    """
    Calculating sum of overall cash register, overall sum by all accounts and overall sum of debt by all accounts.
    It cannot be used without 'calculate_notoriety_and_receipt_sum'!
    """

    # count sum of all notorieties
    checkout_condition = Notoriety.objects.all().values('sum') \
        .aggregate(
        notoriety_income_sum=Sum('sum', filter=Q(type='income'), output_field=FloatField()),
        notoriety_outcome_sum=Sum('sum', filter=Q(type='outcome'), output_field=FloatField()))
    checkout_condition = {
        'sum': (checkout_condition.get('notoriety_income_sum') if checkout_condition.get('notoriety_income_sum') else 0.00) -
               (checkout_condition.get('notoriety_outcome_sum') if checkout_condition.get('notoriety_outcome_sum') else 0.00)
    }

    # count sum by all account's positive rest
    sum_by_account = personal_accounts.aggregate(
        sum=Sum(Case(When(subtraction__lte=0, then=Value(0.0)), default='subtraction', output_field=FloatField())))

    # count debt by all account's negative rest
    debt_by_account = personal_accounts.aggregate(
        debt=-Sum(Case(When(subtraction__gte=0, then=Value(0.0)), default='subtraction', output_field=FloatField())))

    return {'checkout_condition': checkout_condition, 'debt_by_account': debt_by_account,
            'sum_by_account': sum_by_account}


def count_all_totals(personal_accounts: QuerySet):
    """Coalesce calculation of notoriety's and receipt's sum with totals"""
    answer = {}
    answer.update(calculate_notoriety_and_receipt_sum(personal_accounts))
    answer.update(calculate_totals(answer.get('personal_accounts')))
    return answer


def owner_context_data(owner):
    flat_list = Flat.objects\
        .select_related('house', 'tariff')\
        .prefetch_related('tariff__tariffservice_set')\
        .filter(owner=owner)

    return {'flat_list': flat_list}
