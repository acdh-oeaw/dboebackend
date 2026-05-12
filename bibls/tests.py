from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from bibls.models import BibliographicItem
from dboeannotation.urls import router

client = Client()

USER = {"username": "testuser", "password": "somepassword"}


class BiblTestCase(TestCase):
    fixtures = ["dump.json"]

    def setUp(self):
        """Create test user"""
        User.objects.create_user(**USER)

    def get_endpoints(self):
        """Extract bibl endpoints from URL configuration"""
        return [reverse(x.name) for x in router.urls if "list" in x.name]

    def test_001_save(self):
        items = BibliographicItem.objects.all()
        item = items.first()
        self.assertFalse(item.in_zotero)
        item.zotero_key = "https://foo-bar/sumsi"
        item.save()
        self.assertTrue(item.in_zotero)

    def test_002(self):
        endpoints = [x for x in self.get_endpoints() if "bibliographic" in x]
        for x in endpoints:
            response = client.get(x)
            self.assertEqual(
                response.status_code,
                200,
                f"Expected 200 for {x}, got {response.status_code}",
            )
            self.assertIn("results", response.json())
