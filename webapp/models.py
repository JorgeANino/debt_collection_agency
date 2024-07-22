from django.db import models


class CollectionAgency(models.Model):
    name = models.CharField(max_length=255)


class Client(models.Model):
    reference_no = models.UUIDField(primary_key=True)
    agency = models.ForeignKey(
        CollectionAgency, related_name="clients", on_delete=models.CASCADE
    )


class Consumer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    ssn = models.CharField(max_length=11)


class Account(models.Model):
    INACTIVE = "INACTIVE"
    PAID_IN_FULL = "PAID_IN_FULL"
    IN_COLLECTION = "IN_COLLECTION"
    STATUS_CHOICES = [
        (INACTIVE, "Inactive"),
        (PAID_IN_FULL, "Paid in Full"),
        (IN_COLLECTION, "In Collection"),
    ]

    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    consumer = models.ForeignKey(
        Consumer, related_name="accounts", on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        Client, related_name="accounts", on_delete=models.CASCADE
    )
