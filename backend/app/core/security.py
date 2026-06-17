import base64
import hashlib
import hmac
import secrets


class PasswordHasher:
    algorithm = "pbkdf2_sha256"
    iterations = 120_000

    def hash_password(self, password: str, *, salt: str | None = None) -> str:
        salt = salt or secrets.token_urlsafe(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            self.iterations,
        )
        encoded = base64.b64encode(digest).decode("ascii")
        return f"{self.algorithm}${self.iterations}${salt}${encoded}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            algorithm, iterations, salt, encoded_digest = password_hash.split("$", 3)
            if algorithm != self.algorithm:
                return False
            digest = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                int(iterations),
            )
            expected = base64.b64encode(digest).decode("ascii")
            return hmac.compare_digest(expected, encoded_digest)
        except ValueError:
            return False


password_hasher = PasswordHasher()

