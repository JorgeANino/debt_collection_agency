from rest_framework import serializers
from webapp.models import CollectionAgency, Client, Consumer, Account


class CollectionAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionAgency
        fields = ["id", "name"]


class ClientSerializer(serializers.ModelSerializer):
    agency = CollectionAgencySerializer()

    class Meta:
        model = Client
        fields = ["reference_no", "agency"]


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["id", "name", "address", "ssn"]


class AccountSerializer(serializers.ModelSerializer):
    consumer = ConsumerSerializer()
    client = ClientSerializer()

    class Meta:
        model = Account
        fields = ["id", "balance", "status", "consumer", "client"]
