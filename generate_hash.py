import base64
import hashlib
import argparse

ALGORITHM = "pbkdf2_sha256"

iterations = 600000

salt = "123"

password = "admin"

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--password", help="Enter password", type=str)
parser.add_argument("-i", "--iterations", help="Enter iterations number", type=int)
parser.add_argument("-s", "--salt", help="Enter salt", type=int)


args = parser.parse_args()

if args.password:
    password = args.password

if args.iterations:
    iterations = args.iterations

if args.salt:
    salt = args.salt

pw_hash = hashlib.pbkdf2_hmac(
    "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
)


b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()

print(f"{ALGORITHM}${iterations}${salt}${b64_hash}")
