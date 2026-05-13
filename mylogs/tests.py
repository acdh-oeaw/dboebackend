from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from belege.models import Beleg
from mylogs.models import LogEntry


class LogEntryApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="secret"
        )
        self.beleg = Beleg.objects.create(dboe_id="test-1")
        self.log = LogEntry.objects.create(beleg=self.beleg, username="alice")

    def test_list_and_detail_include_all_fields(self):
        list_response = self.client.get(reverse("logs-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data["results"]), 1)

        expected_fields = {"id", "beleg", "created_at", "username", "payload"}
        self.assertEqual(set(list_response.data["results"][0].keys()), expected_fields)

        detail_response = self.client.get(reverse("logs-detail", args=[self.log.pk]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(detail_response.data.keys()), expected_fields)

    def test_post_writes_only_allowed_fields(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("logs-list"),
            {
                "beleg": self.beleg.pk,
                "username": "bob",
                "payload": "client-payload",
                "created_at": "2000-01-01T00:00:00Z",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = LogEntry.objects.get(pk=response.data["id"])
        self.assertEqual(created.beleg_id, self.beleg.pk)
        self.assertEqual(created.username, "bob")
        self.assertNotEqual(created.payload, "client-payload")

    def test_list_can_be_filtered_by_beleg(self):
        other_beleg = Beleg.objects.create(dboe_id="test-2")
        LogEntry.objects.create(beleg=other_beleg, username="charlie")

        response = self.client.get(reverse("logs-list"), {"beleg": self.beleg.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["beleg"], self.beleg.pk)
