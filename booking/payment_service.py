import logging
import requests

logger = logging.getLogger(__name__)


def process_payment(booking_id, payment_status):
    """
    Send payment information to a mock external payment service.
    """

    payload = {
        "booking_id": booking_id,
        "payment_status": payment_status,
    }

    try:
        response = requests.post(
            "https://httpbin.org/post",
            json=payload,
            timeout=5,
        )

        response.raise_for_status()

        logger.info(
            "Payment sent to mock service for booking %s",
            booking_id,
        )

        return True

    except requests.exceptions.RequestException as exc:
        logger.error(
            "Payment service failed for booking %s: %s",
            booking_id,
            exc,
        )

        return False