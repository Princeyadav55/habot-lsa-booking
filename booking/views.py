from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import BookingRequest, LSAProfile, Payment
from .payment_service import process_payment

from .serializers import (
    BookingRequestSerializer,
    LSAProfileSerializer
)


class BookingCreateView(generics.CreateAPIView):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer


class LSASearchView(generics.ListAPIView):
    serializer_class = LSAProfileSerializer

    def get_queryset(self):
        skill = self.request.query_params.get("skill")

        queryset = LSAProfile.objects.filter(
            is_available=True
        )

        if skill:
            queryset = queryset.filter(
                skills__icontains=f'"{skill}"'
            )

        return queryset


class PaymentWebhookView(APIView):

    def post(self, request):
        booking_id = request.data.get("booking_id")
        payment_status = request.data.get("payment_status")

        booking = get_object_or_404(
            BookingRequest,
            id=booking_id
        )

        if payment_status == "SUCCESS":
            booking.status = "CONFIRMED"

        elif payment_status == "FAILED":
            booking.status = "FAILED"

        else:
            return Response(
                {"error": "Invalid payment status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment_processed = process_payment(
            booking.id,
            payment_status
        )

        if not payment_processed:
            return Response(
                {"error": "Payment service is unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        booking.save()

        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                "amount": 0,
                "status": payment_status,
                "transaction_id": f"TXN-{booking.id}",
            }
        )

        if not created:
            payment.status = payment_status
            payment.save()

        return Response(
            {
                "message": "Payment processed successfully.",
                "booking_id": booking.id,
                "booking_status": booking.status,
                "payment_status": payment.status,
            },
            status=status.HTTP_200_OK
        )