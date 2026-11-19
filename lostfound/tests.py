
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from .models import Item


class ItemModelTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="teststudent",
            password="testpassword123"
        )

        self.item = Item.objects.create(
            user=self.user,
            item_name="Laptop",
            item_type="LOST",
            category="Electronics",
            description="Black HP laptop",
            date=date.today(),
            location="LCWU Library"
        )

    def test_item_creation(self):
        self.assertEqual(self.item.item_name, "Laptop")

    def test_item_default_status(self):
        self.assertEqual(self.item.status, "ACTIVE")

    def test_item_string_representation(self):
        self.assertEqual(str(self.item), "Laptop - LOST")
