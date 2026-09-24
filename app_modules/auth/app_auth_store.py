import base64
import hashlib
import hmac
import json

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False


def hash_password(password):
    """Securely hash password using bcrypt (cost factor 12) with SHA-256 fallback."""
    if not password:
        return ""
    if HAS_BCRYPT:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password, stored_hash):
    """Verify password against bcrypt hash, with backward-compatibility for legacy SHA-256."""
    if not plain_password or not stored_hash:
        return False
    if str(stored_hash).startswith("$2"):
        if HAS_BCRYPT:
            try:
                return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash.encode("utf-8"))
            except Exception:
                return False
        return False
    # Legacy SHA-256 comparison using constant-time comparison
    sha = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(sha, str(stored_hash).strip())


def load_auth_accounts(auth_store_path):
    if not auth_store_path.exists():
        return []

    try:
        return json.loads(auth_store_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_auth_accounts(auth_store_path, accounts, safe_int):
    auth_store_path.parent.mkdir(parents=True, exist_ok=True)
    # Ensure plaintext passwords are never persisted to disk
    sanitized_accounts = []
    for acct in accounts:
        cleaned = dict(acct)
        cleaned.pop("password", None)
        sanitized_accounts.append(cleaned)

    sorted_accounts = sorted(
        sanitized_accounts,
        key=lambda item: (
            safe_int(item.get("staff_code"), 9999),
            str(item.get("name", "")).lower(),
        ),
    )
    auth_store_path.write_text(json.dumps(sorted_accounts, indent=2), encoding="utf-8")


def find_auth_account(auth_store_path, identifier, role=None):
    normalized = str(identifier or "").strip().lower()
    if not normalized:
        return None

    for account in load_auth_accounts(auth_store_path):
        username = str(account.get("username", "")).strip().lower()
        email = str(account.get("email", "")).strip().lower()
        staff_code = str(account.get("staff_code", "")).strip().lower()
        if normalized not in {username, email, staff_code}:
            continue
        if role and account.get("role") != role:
            continue
        return account
    return None


def generate_staff_code(accounts, safe_int):
    used_codes = {
        safe_int(account.get("staff_code"), 0)
        for account in accounts
        if safe_int(account.get("staff_code"), 0) > 0
    }
    next_code = 1
    while next_code in used_codes:
        next_code += 1
    return f"{next_code:03d}"
