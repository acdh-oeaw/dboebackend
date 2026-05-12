from django.contrib.auth.models import User
from django.test import Client, TestCase

from bibls.models import BibliographicItem

client = Client()

USER = {"username": "testuser", "password": "somepassword"}


class BiblTestCase(TestCase):
    fixtures = ["dump.json"]

    def setUp(self):
        """Create test user"""
        User.objects.create_user(**USER)

    def test_001_save(self):
        items = BibliographicItem.objects.all()
        item = items.first()
        self.assertFalse(item.in_zotero)
        item.zotero_key = "https://foo-bar/sumsi"
        item.save()
        self.assertTrue(item.in_zotero)
