from django.db import models


class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class LSAProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    skills = models.JSONField(default=list)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BookingRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("FAILED", "Failed"),
    ]

    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    lsa = models.ForeignKey(
        LSAProfile,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    session_start = models.DateTimeField()
    session_end = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.session_start >= self.session_end:
            raise ValidationError(
                "Session end must be after session start."
            )

        overlapping_booking = BookingRequest.objects.filter(
            lsa=self.lsa,
            session_start__lt=self.session_end,
            session_end__gt=self.session_start,
            status__in=["PENDING", "CONFIRMED"],
        ).exclude(pk=self.pk).exists()

        if overlapping_booking:
            raise ValidationError(
                "This LSA is already booked for the selected time."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} - {self.lsa.name}"


class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    booking = models.OneToOneField(
        BookingRequest,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"