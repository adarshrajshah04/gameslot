from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class DashboardHolidayViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="calendar-test",
            password="test-password",
        )
        self.client.force_login(self.user)
        self.url = reverse("dashboard_holidays")

    def test_returns_festival_dates_for_requested_year(self):
        response = self.client.get(self.url, {"year": 2027})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["holidays"]["2027-03-22"], "Holi")

    def test_rejects_year_outside_supported_range(self):
        response = self.client.get(self.url, {"year": 2036})

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_rejects_invalid_year(self):
        response = self.client.get(self.url, {"year": "not-a-year"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_requires_login(self):
        self.client.logout()

        response = self.client.get(self.url, {"year": 2027})

        self.assertEqual(response.status_code, 302)
