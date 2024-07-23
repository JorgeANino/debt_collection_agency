import csv

from django.db.models import Prefetch

from rest_framework import generics, status, views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from webapp.models import Client, CollectionAgency, Consumer, Account
from webapp.serializers import AccountSerializer
from webapp.filters import AccountFilter


class AccountListView(generics.ListAPIView):
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter

    def get_queryset(self):
        clients_with_agencies = Client.objects.select_related('agency')
        return Account.objects.select_related('consumer').prefetch_related(
            Prefetch('client', queryset=clients_with_agencies)
        ).all()


class CSVUploadView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.data.get("file")
        if not file:
            return Response(
                {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )

        agency_name = request.data.get("agency_name")
        if not agency_name:
            return Response(
                {"error": "Agency name not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        agency, _ = CollectionAgency.objects.get_or_create(
            name=agency_name)

        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        consumers = {}
        accounts_to_create = []
        clients = {}

        for row in reader:
            reference_no = row["client reference no"]
            if reference_no not in clients:
                clients[reference_no], _ = Client.objects.get_or_create(
                    reference_no=reference_no, agency=agency
                )
            client = clients[reference_no]

            consumer_key = (row["consumer name"],
                            row["consumer address"], row["ssn"])
            if consumer_key not in consumers:
                consumers[consumer_key], _ = Consumer.objects.get_or_create(
                    name=row["consumer name"],
                    address=row["consumer address"],
                    ssn=row["ssn"],
                )
            consumer = consumers[consumer_key]
            accounts_to_create.append(
                Account(
                    balance=row["balance"],
                    status=row["status"],
                    consumer=consumer,
                    client=client,
                )
            )

        Account.objects.bulk_create(accounts_to_create)

        return Response(
            {"status": "Data ingested successfully"}, status=status.HTTP_201_CREATED
        )
