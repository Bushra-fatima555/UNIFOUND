
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from .models import Item, Claim


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


class LoginRequiredTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="student",
            password="testpassword123"
        )

        self.item = Item.objects.create(
            user=self.user,
            item_name="Test Laptop",
            item_type="FOUND",
            category="Electronics",
            description="Black laptop",
            date=date.today(),
            location="LCWU Library"
        )

    def test_item_list_requires_login(self):
        response = self.client.get('/lostfound/items/')

        self.assertRedirects(
            response,
            '/login/?next=/lostfound/items/'
        )

    def test_create_item_requires_login(self):
        response = self.client.get('/lostfound/report/')

        self.assertRedirects(
            response,
            '/login/?next=/lostfound/report/'
        )

    def test_item_detail_requires_login(self):
        response = self.client.get(
            f'/lostfound/item/{self.item.id}/'
        )

        self.assertRedirects(
            response,
            f'/login/?next=/lostfound/item/{self.item.id}/'
        )


class ClaimApprovalTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.owner = User.objects.create_user(
            username="owner",
            password="testpassword123"
        )

        self.claimant1 = User.objects.create_user(
            username="claimant1",
            password="testpassword123"
        )

        self.claimant2 = User.objects.create_user(
            username="claimant2",
            password="testpassword123"
        )

        self.other_user = User.objects.create_user(
            username="unauthorized",
            password="testpassword123"
        )

        self.item = Item.objects.create(
            user=self.owner,
            item_name="Found Laptop",
            item_type="FOUND",
            category="Electronics",
            description="Black HP laptop",
            date=date.today(),
            location="LCWU Library",
            status="CLAIM_PENDING"
        )

        self.claim1 = Claim.objects.create(
            item=self.item,
            claimant=self.claimant1,
            claim_message="This is my laptop."
        )

        self.claim2 = Claim.objects.create(
            item=self.item,
            claimant=self.claimant2,
            claim_message="I lost this laptop."
        )

    def test_only_one_claim_can_be_approved(self):

        self.client.force_login(self.owner)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/update/',
            {'action': 'approve'}
        )

        self.client.post(
            f'/lostfound/claim/{self.claim2.id}/update/',
            {'action': 'approve'}
        )

        self.claim1.refresh_from_db()
        self.claim2.refresh_from_db()

        approved_claims = Claim.objects.filter(
            item=self.item,
            status='APPROVED'
        ).count()

        self.assertEqual(approved_claims, 1)
        self.assertEqual(self.claim1.status, 'APPROVED')
        self.assertEqual(self.claim2.status, 'PENDING')

    def test_reject_claim_updates_item_status(self):

        self.client.force_login(self.owner)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/update/',
            {'action': 'reject'}
        )

        self.claim1.refresh_from_db()
        self.item.refresh_from_db()

        self.assertEqual(self.claim1.status, 'REJECTED')
        self.assertEqual(self.item.status, 'CLAIM_PENDING')

    def test_item_becomes_active_after_all_claims_rejected(self):

        self.client.force_login(self.owner)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/update/',
            {'action': 'reject'}
        )

        self.client.post(
            f'/lostfound/claim/{self.claim2.id}/update/',
            {'action': 'reject'}
        )

        self.claim1.refresh_from_db()
        self.claim2.refresh_from_db()
        self.item.refresh_from_db()

        self.assertEqual(self.claim1.status, 'REJECTED')
        self.assertEqual(self.claim2.status, 'REJECTED')
        self.assertEqual(self.item.status, 'ACTIVE')

    def test_item_returned_after_both_confirmations(self):

        self.claim1.status = 'APPROVED'
        self.claim1.save()

        self.client.force_login(self.claimant1)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/confirm/'
        )

        self.claim1.refresh_from_db()
        self.item.refresh_from_db()

        self.assertTrue(self.claim1.claimant_confirmed)
        self.assertFalse(self.claim1.finder_confirmed)
        self.assertNotEqual(self.item.status, 'RETURNED')

        self.client.force_login(self.owner)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/confirm/'
        )

        self.claim1.refresh_from_db()
        self.item.refresh_from_db()

        self.assertTrue(self.claim1.finder_confirmed)
        self.assertEqual(self.claim1.status, 'APPROVED')
        self.assertEqual(self.item.status, 'RETURNED')

    def test_other_user_cannot_approve_claim(self):

        self.client.force_login(self.other_user)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/update/',
            {'action': 'approve'}
        )

        self.claim1.refresh_from_db()

        self.assertEqual(self.claim1.status, 'PENDING')

    def test_other_user_cannot_reject_claim(self):

        self.client.force_login(self.other_user)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/update/',
            {'action': 'reject'}
        )

        self.claim1.refresh_from_db()

        self.assertEqual(self.claim1.status, 'PENDING')

    def test_other_user_cannot_confirm_return(self):

        self.claim1.status = 'APPROVED'
        self.claim1.save()

        self.client.force_login(self.other_user)

        self.client.post(
            f'/lostfound/claim/{self.claim1.id}/confirm/'
        )

        self.claim1.refresh_from_db()
        self.item.refresh_from_db()

        self.assertFalse(self.claim1.claimant_confirmed)
        self.assertFalse(self.claim1.finder_confirmed)
        self.assertNotEqual(self.item.status, 'RETURNED')


class ItemEditDeleteTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.owner = User.objects.create_user(
            username="itemowner",
            password="testpassword123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword123"
        )

        self.item = Item.objects.create(
            user=self.owner,
            item_name="Old Laptop",
            item_type="LOST",
            category="Electronics",
            description="Black HP laptop",
            date=date.today(),
            location="Old Library"
        )

    def test_owner_can_edit_item(self):

        self.client.force_login(self.owner)

        self.client.post(
            f'/lostfound/item/{self.item.id}/edit/',
            {
                'item_name': 'Updated Laptop',
                'item_type': 'LOST',
                'category': 'Electronics',
                'description': 'Updated laptop description',
                'date': date.today().isoformat(),
                'location': 'New Library'
            }
        )

        self.item.refresh_from_db()

        self.assertEqual(self.item.item_name, 'Updated Laptop')
        self.assertEqual(self.item.location, 'New Library')

    def test_other_user_cannot_edit_item(self):

        self.client.force_login(self.other_user)

        self.client.post(
            f'/lostfound/item/{self.item.id}/edit/',
            {
                'item_name': 'Hacked Laptop',
                'item_type': 'LOST',
                'category': 'Electronics',
                'description': 'Changed description',
                'date': date.today().isoformat(),
                'location': 'New Location'
            }
        )

        self.item.refresh_from_db()

        self.assertEqual(self.item.item_name, 'Old Laptop')
        self.assertEqual(self.item.location, 'Old Library')

    def test_owner_can_delete_item(self):

        self.client.force_login(self.owner)

        self.client.post(
            f'/lostfound/item/{self.item.id}/delete/'
        )

        self.assertFalse(
            Item.objects.filter(id=self.item.id).exists()
        )

    def test_other_user_cannot_delete_item(self):

        self.client.force_login(self.other_user)

        self.client.post(
            f'/lostfound/item/{self.item.id}/delete/'
        )

        self.assertTrue(
            Item.objects.filter(id=self.item.id).exists()
        )
