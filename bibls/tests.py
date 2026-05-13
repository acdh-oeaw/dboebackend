from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from tqdm import tqdm

from bibls.models import BibliographicItem, BibliographicType
from dboeannotation.urls import router

client = Client()

USER = {"username": "testuser", "password": "somepassword"}


class BiblTestCase(TestCase):
    fixtures = ["dump.json"]

    def setUp(self):
        """Create test user"""
        User.objects.create_user(**USER)

    def get_list_view_endpoints(self):
        """Extract bibl endpoints from URL configuration"""
        return [reverse(x.name) for x in router.urls if x.name.endswith("-list")]

    def test_001_save(self):
        items = BibliographicItem.objects.all()
        item = items.first()
        self.assertFalse(item.in_zotero)
        item.zotero_key = "https://foo-bar/sumsi"
        item.save()
        self.assertTrue(item.in_zotero)

    def test_002_list_views(self):
        endpoints = [x for x in self.get_list_view_endpoints()]
        with self.settings(DEBUG=True):
            for x in set(endpoints):
                response = client.get(x)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Expected 200 for {x}, got {response.status_code}",
                )
        for x in tqdm(set(endpoints), total=len(endpoints)):
            response = client.get(x)
            self.assertEqual(
                response.status_code,
                200,
                f"Expected 200 for {x}, got {response.status_code}",
            )

    def test_03_custom_string_methods(self):
        item = BibliographicType.objects.create(main_type="Literatur")
        self.assertEqual(str(item), "Literatur")

        item = BibliographicType.objects.create(
            main_type="Literatur", sub_type="Fachliteratur"
        )
        self.assertEqual(str(item), "Literatur >> Fachliteratur")

        item = BibliographicType.objects.create(
            main_type="Literatur",
            sub_type="Fachliteratur",
            specification="Dissertation",
        )
        self.assertEqual(str(item), "Literatur >> Fachliteratur >> Dissertation")

        bibl = BibliographicItem.objects.create(
            sigle="foo", short_title="bar", full_title="roo", bibl_type=item
        )
        self.assertEqual(str(bibl), "bar")
