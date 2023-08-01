import base64
import hashlib

ALGORITHM = "pbkdf2_sha256"

iterations = 600000

salt = "123"

password = "admin"

pw_hash = hashlib.pbkdf2_hmac("sha256",password.encode("utf-8"),salt.encode("utf-8"),iterations)

b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()

print(f"{ALGORITHM}${iterations}${salt}${b64_hash}")

