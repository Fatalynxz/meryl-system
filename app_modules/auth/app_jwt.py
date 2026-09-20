import base64
import hmac
import hashlib
import json
import os
import time

try:
    import jwt as pyjwt
    HAS_PYJWT = True
except ImportError:
    HAS_PYJWT = False


def get_jwt_secret():
    """Retrieve secret key for signing JWT tokens."""
    return os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY") or "meryl-secure-jwt-signing-key-2026-production"


def _b64encode_no_padding(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64decode_with_padding(data_str: str) -> bytes:
    padding = 4 - (len(data_str) % 4)
    if padding and padding != 4:
        data_str += "=" * padding
    return base64.urlsafe_b64decode(data_str)


def create_jwt_token(payload: dict, expires_in_seconds: int = 604800) -> str:
    """
    Generate an RFC 7519 compliant HS256 JWT token.
    Defaults to 7 days (604800s) expiration.
    """
    secret = get_jwt_secret()
    now = int(time.time())
    token_payload = {
        **payload,
        "iat": now,
        "exp": now + expires_in_seconds,
    }

    if HAS_PYJWT:
        return pyjwt.encode(token_payload, secret, algorithm="HS256")

    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _b64encode_no_padding(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64encode_no_padding(json.dumps(token_payload, separators=(",", ":")).encode("utf-8"))

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = _b64encode_no_padding(signature)

    return f"{header_b64}.{payload_b64}.{sig_b64}"


def verify_jwt_token(token: str) -> dict:
    """
    Verify and decode an HS256 JWT token.
    Returns the decoded payload dict if valid.
    Raises ValueError on invalid token, signature mismatch, or expiration.
    """
    if not token or not isinstance(token, str):
        raise ValueError("Token is required")

    clean_token = token.strip()
    if clean_token.lower().startswith("bearer "):
        clean_token = clean_token[7:].strip()

    secret = get_jwt_secret()

    if HAS_PYJWT:
        try:
            return pyjwt.decode(clean_token, secret, algorithms=["HS256"])
        except pyjwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except pyjwt.InvalidTokenError as err:
            raise ValueError(f"Invalid token: {err}")

    parts = clean_token.split(".")
    if len(parts) != 3:
        raise ValueError("Malformed JWT token structure")

    header_b64, payload_b64, sig_b64 = parts

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    expected_sig_b64 = _b64encode_no_padding(expected_sig)

    if not hmac.compare_digest(sig_b64, expected_sig_b64):
        raise ValueError("Invalid token signature")

    try:
        payload_bytes = _b64decode_with_padding(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception as err:
        raise ValueError(f"Unable to parse token payload: {err}")

    exp = payload.get("exp")
    if exp and int(exp) < int(time.time()):
        raise ValueError("Token has expired")

    return payload

