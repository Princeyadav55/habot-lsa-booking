from rest_framework import serializers
from .models import Parent, LSAProfile, BookingRequest


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ["id", "name", "email", "phone"]


class LSAProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LSAProfile
        fields = ["id", "name", "email", "skills", "is_available"]


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = [
            "id",
            "parent",
            "lsa",
            "session_start",
            "session_end",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, attrs):
        session_start = attrs.get("session_start")
        session_end = attrs.get("session_end")

        if session_start >= session_end:
            raise serializers.ValidationError(
                "session_end must be after session_start."
            )

        lsa = attrs.get("lsa")

        overlapping_booking = BookingRequest.objects.filter(
            lsa=lsa,
            session_start__lt=session_end,
            session_end__gt=session_start,
            status__in=["PENDING", "CONFIRMED"],
        ).exists()

        if overlapping_booking:
            raise serializers.ValidationError(
                "This LSA is already booked for the selected time."
            )

        return attrs 