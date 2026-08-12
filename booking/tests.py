from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Parent, LSAProfile, BookingRequest


class BookingAPITestCase(APITestCase):

    def setUp(self):
        self.parent = Parent.objects.create(
            name="Test Parent",
            email="parent@test.com",
            phone="9999999999"
        )

        self.lsa = LSAProfile.objects.create(
            name="Test LSA",
            email="lsa@test.com",
            skills=["ADHD", "Dyslexia"],
            is_available=True
        )

    def test_lsa_search(self):
        response = self.client.get("/api/v1/lsas/search/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_lsa_search_by_skill(self):
        response = self.client.get(
            "/api/v1/lsas/search/?skill=ADHD"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["name"],
            "Test LSA"
        )

    def test_booking_create(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "parent": self.parent.id,
                "lsa": self.lsa.id,
                "session_start": "2026-08-20T10:00:00Z",
                "session_end": "2026-08-20T11:00:00Z"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookingRequest.objects.count(), 1)

    def test_invalid_session_time(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "parent": self.parent.id,
                "lsa": self.lsa.id,
                "session_start": "2026-08-20T11:00:00Z",
                "session_end": "2026-08-20T10:00:00Z"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_duplicate_booking(self):
        data = {
            "parent": self.parent.id,
            "lsa": self.lsa.id,
            "session_start": "2026-08-20T10:00:00Z",
            "session_end": "2026-08-20T11:00:00Z"
        }

        first_response = self.client.post(
            "/api/v1/bookings/",
            data,
            format="json"
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED
        )

        second_response = self.client.post(
            "/api/v1/bookings/",
            data,
            format="json"
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_payment_webhook_success(self):
        booking = BookingRequest.objects.create(
            parent=self.parent,
            lsa=self.lsa,
            session_start="2026-08-21T10:00:00Z",
            session_end="2026-08-21T11:00:00Z"
        )

        response = self.client.post(
            "/api/v1/payments/webhook/",
            {
                "booking_id": booking.id,
                "payment_status": "SUCCESS"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            "CONFIRMED"
        )