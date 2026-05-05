import hmac
import hashlib
from django.conf import settings

def verify_signature(request):
    signature = request.headers.get("x-signature")
    request_id = request.headers.get("x-request-id")

    if not signature or not request_id:
        return False

    data = request.body

    generated_signature = hmac.new(
        settings.MP_WEBHOOK_SECRET.encode(),
        data,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(generated_signature, signature)