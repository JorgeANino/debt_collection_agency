from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from webapp.models import CollectionAgency, Client, Consumer, Account

ACCOUNTS_URL = "/api/v1/accounts/"


class AccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.agency = CollectionAgency.objects.create(name="Test Agency")
        self.client_instance = Client.objects.create(
            reference_no="ffeb5d88-e5af-45f0-9637-16ea469c58c0", agency=self.agency
        )
        self.consumer1 = Consumer.objects.create(
            name="John Doe", address="123 Main St", ssn="123-45-6789"
        )
        self.consumer2 = Consumer.objects.create(
            name="Jane Doe", address="456 Elm St", ssn="987-65-4321"
        )

        Account.objects.create(
            balance=500.00,
            status="IN_COLLECTION",
            consumer=self.consumer1,
            client=self.client_instance,
        )
        Account.objects.create(
            balance=1000.00,
            status="PAID_IN_FULL",
            consumer=self.consumer2,
            client=self.client_instance,
        )

    def test_get_all_accounts(self):
        response = self.client.get(ACCOUNTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_accounts_by_min_balance(self):
        response = self.client.get(f"{ACCOUNTS_URL}?min_balance=600")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["balance"], "1000.00")

    def test_filter_accounts_by_max_balance(self):
        response = self.client.get(f"{ACCOUNTS_URL}?max_balance=600")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["balance"], "500.00")

    def test_filter_accounts_by_consumer_name(self):
        response = self.client.get(f"{ACCOUNTS_URL}?consumer_name=jane")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"]
                         [0]["consumer"]["name"], "Jane Doe")

    def test_filter_accounts_by_status(self):
        response = self.client.get(f"{ACCOUNTS_URL}?status=PAID_IN_FULL")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["status"], "PAID_IN_FULL")

    def test_filter_accounts_by_agency_name(self):
        response = self.client.get(f"{ACCOUNTS_URL}?agency_name=Test Agency")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_accounts_by_client_reference_no(self):
        response = self.client.get(
            f"{ACCOUNTS_URL}?client_reference_no=ffeb5d88-e5af-45f0-9637-16ea469c58c0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_accounts_by_consumer_ssn(self):
        response = self.client.get(f"{ACCOUNTS_URL}?consumer_ssn=123-45-6789")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"]
                         [0]["consumer"]["ssn"], "123-45-6789")

    def test_filter_accounts_by_multiple_criteria(self):
        response = self.client.get(
            f"{ACCOUNTS_URL}?min_balance=600&status=PAID_IN_FULL&consumer_name=jane"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["balance"], "1000.00")
        self.assertEqual(response.data["results"][0]["status"], "PAID_IN_FULL")
        self.assertEqual(response.data["results"]
                         [0]["consumer"]["name"], "Jane Doe")

    def test_filter_accounts_by_multiple_agencies(self):
        # Create a second agency and associated client and accounts
        second_agency = CollectionAgency.objects.create(name="Second Agency")
        second_client = Client.objects.create(
            reference_no="d984a3b4-d331-4857-8e6f-b44bad2567aa", agency=second_agency
        )
        consumer3 = Consumer.objects.create(
            name="Alice Smith", address="789 Pine St", ssn="555-55-5555"
        )
        Account.objects.create(
            balance=1500.00,
            status="IN_COLLECTION",
            consumer=consumer3,
            client=second_client,
        )

        # Test filtering accounts by the first agency
        response = self.client.get(f"{ACCOUNTS_URL}?agency_name=Test Agency")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        # Test filtering accounts by the second agency
        response = self.client.get(f"{ACCOUNTS_URL}?agency_name=Second Agency")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"]
                         [0]["consumer"]["name"], "Alice Smith")

    def test_filter_accounts_across_multiple_agencies(self):
        # Create a second agency and associated client and accounts
        second_agency = CollectionAgency.objects.create(name="Second Agency")
        second_client = Client.objects.create(
            reference_no="d984a3b4-d331-4857-8e6f-b44bad2567aa", agency=second_agency
        )
        consumer3 = Consumer.objects.create(
            name="Alice Smith", address="789 Pine St", ssn="555-55-5555"
        )
        Account.objects.create(
            balance=1500.00,
            status="IN_COLLECTION",
            consumer=consumer3,
            client=second_client,
        )

        # Test filtering accounts by consumer name across multiple agencies
        response = self.client.get(
            f"{ACCOUNTS_URL}?agency_name={self.agency.name},{second_agency.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertIn("John Doe", [account["consumer"]["name"]
                      for account in response.data["results"]])
        self.assertIn("Jane Doe", [account["consumer"]["name"]
                      for account in response.data["results"]])
        self.assertIn("Alice Smith", [account["consumer"]["name"]
                      for account in response.data["results"]])


class UploadCSVTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.agency = CollectionAgency.objects.create(name="Test Agency")

    def test_upload_csv(self):
        url = "/api/v1/upload/"
        csv_content = (
            "client reference no,balance,status,consumer name,consumer address,ssn\n"
            'ffeb5d88-e5af-45f0-9637-16ea469c58c0,1200.00,IN_COLLECTION,Anna Smith,"789 Oak St, Somecity, AA 12345",123-45-6780\n'
        )
        data = {
            "file": SimpleUploadedFile(
                "accounts.csv", csv_content.encode(), content_type="text/csv"
            ),
            "agency_name": self.agency.name,
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(
            Account.objects.filter(consumer__name="Anna Smith").exists(), True
        )

    def test_upload_csv_to_multiple_agencies(self):
        # Create a second agency
        second_agency = CollectionAgency.objects.create(name="Second Agency")

        # Upload CSV for the first agency
        url = "/api/v1/upload/"
        csv_content_first = (
            "client reference no,balance,status,consumer name,consumer address,ssn\n"
            'ffeb5d88-e5af-45f0-9637-16ea469c58c0,1200.00,IN_COLLECTION,Anna Smith,"789 Oak St, Somecity, AA 12345",123-45-6780\n'
        )
        data_first = {
            "file": SimpleUploadedFile(
                "accounts_first.csv", csv_content_first.encode(), content_type="text/csv"
            ),
            "agency_name": self.agency.name,
        }
        response_first = self.client.post(url, data_first, format="multipart")
        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(
            Account.objects.filter(
                consumer__name="Anna Smith", client__agency=self.agency).exists(), True
        )

        # Upload CSV for the second agency
        csv_content_second = (
            "client reference no,balance,status,consumer name,consumer address,ssn\n"
            'd984a3b4-d331-4857-8e6f-b44bad2567aa,1300.00,PAID_IN_FULL,Bob Johnson,"321 Elm St, Anothercity, BB 54321",678-90-1234\n'
        )
        data_second = {
            "file": SimpleUploadedFile(
                "accounts_second.csv", csv_content_second.encode(), content_type="text/csv"
            ),
            "agency_name": second_agency.name,
        }
        response_second = self.client.post(
            url, data_second, format="multipart")
        self.assertEqual(response_second.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(
            Account.objects.filter(
                consumer__name="Bob Johnson", client__agency=second_agency).exists(), True
        )
