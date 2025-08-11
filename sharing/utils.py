# sharing/utils.py
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings

signer = TimestampSigner()

def generate_share_link(share_id, max_age_seconds=None):
    """
    Generates a signed URL token for the given share ID.
    If max_age_seconds is provided, it will be used for verification later.
    """
    token = signer.sign(str(share_id))
    return f"/sharing/access/{token}/"

def verify_share_link(token, max_age_seconds=None):
    """
    Verifies the token and returns the share ID if valid.
    Raises SignatureExpired if expired, BadSignature if tampered.
    """
    try:
        unsigned = signer.unsign(token, max_age=max_age_seconds)
        return unsigned
    except SignatureExpired:
        raise
    except BadSignature:
        raise
