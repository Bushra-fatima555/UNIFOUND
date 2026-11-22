from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from claims.models import Claim, Feedback


class AdminPanelTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            is_staff=True
        )

        self.student = User.objects.create_user(
            username='teststudent',
            password='testpass123',
            is_staff=False
        )

    def test_admin_can_open_dashboard(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_student_cannot_open_dashboard(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_open_manage_students(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('manage_students'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_open_manage_claims(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('manage_claims'))
        self.assertEqual(response.status_code, 200)

    def test_claim_search(self):
        Claim.objects.create(
            claimant_name='Test Student',
            item_name='Test Wallet',
            claim_message='Testing claim'
        )

        self.client.force_login(self.admin)
        response = self.client.get(
            reverse('manage_claims'),
            {'search': 'Test Wallet'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wallet')

    def test_admin_can_open_lostfound_reports(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse('manage_lostfound_reports')
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_can_open_lostfound_claims(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse('manage_lostfound_claims')
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_can_open_feedback(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse('manage_feedback')
        )
        self.assertEqual(response.status_code, 200)

    def test_feedback_search(self):
        Feedback.objects.create(
            student_name='Test Student',
            email='test@example.com',
            subject='Wallet Found',
            message='Testing feedback'
        )

        self.client.force_login(self.admin)
        response = self.client.get(
            reverse('manage_feedback'),
            {'search': 'Wallet Found'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wallet Found')

    def test_student_cannot_open_feedback(self):
        self.client.force_login(self.student)
        response = self.client.get(
            reverse('manage_feedback')
        )
        self.assertEqual(response.status_code, 302)

    def test_claim_status_update_requires_post(self):
        claim = Claim.objects.create(
            claimant_name='Test Student',
            item_name='Test Book',
            claim_message='Testing'
        )

        self.client.force_login(self.admin)
        response = self.client.get(
            f'/admin-dashboard/update-claim/{claim.id}/'
        )

        self.assertEqual(response.status_code, 405)

    def test_student_status_update_requires_post(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse(
                'toggle_student_status',
                args=[self.student.id]
            )
        )

        self.assertEqual(response.status_code, 405)