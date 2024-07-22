import django_filters
from webapp.models import Account


class AccountFilter(django_filters.FilterSet):
    min_balance = django_filters.NumberFilter(
        field_name="balance", lookup_expr="gte")
    max_balance = django_filters.NumberFilter(
        field_name="balance", lookup_expr="lte")
    consumer_name = django_filters.CharFilter(
        field_name="consumer__name", lookup_expr="icontains")
    status = django_filters.CharFilter(
        field_name="status", lookup_expr="iexact")
    agency_name = django_filters.CharFilter(
        field_name="client__agency__name", lookup_expr="icontains")
    client_reference_no = django_filters.UUIDFilter(
        field_name="client__reference_no")
    consumer_ssn = django_filters.CharFilter(
        field_name="consumer__ssn", lookup_expr="iexact")

    class Meta:
        model = Account
        fields = ["min_balance", "max_balance", "consumer_name",
                  "status", "agency_name", "client_reference_no", "consumer_ssn"]
