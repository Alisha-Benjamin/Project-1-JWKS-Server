from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64

app = Flask(__name__)

# Key Management
class Key:
    def __init__(self, kid, key, expires):
        self.kid = kid
        self.key = key
        self.expires = expires

    def is_valid(self):
        return datetime.now() < self.expires

keys = {}

def generate_key(kid, expires_in):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    expires = datetime.now() + expires_in
    keys[kid] = Key(
        kid=kid,
        key=private_key,
        expires=expires
    )

def get_valid_keys():
    return {kid: key for kid, key in keys.items() if key.is_valid()}

def key_to_jwk(key):
    public_numbers = key.key.public_key().public_numbers()
    return {
        "kid": key.kid,
        "kty": "RSA",
        "n": base64.urlsafe_b64encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, byteorder='big')).decode('utf-8').rstrip('='),  # Base64Url encoding
        "e": base64.urlsafe_b64encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, byteorder='big')).decode('utf-8').rstrip('='),  # Base64Url encoding
    }

# Generate keys
generate_key("key1", timedelta(days=1))
generate_key("key2", timedelta(days=-1))  # Expired key

@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    valid_keys = get_valid_keys()
    jwks = {
        "keys": [key_to_jwk(key) for key in valid_keys.values()]
    }
    return jsonify(jwks)

def issue_jwt(kid, expired=False):
    key = keys.get(kid)

    # Debugging output
    if not key:
        print(f"Key with kid '{kid}' is not found.")
        return None

    try:
        # Set expiration based on whether the token should be expired
        if expired:
            expiration = datetime.now() - timedelta(days=1)  # Expiry in the past
        else:
            expiration = datetime.now() + timedelta(days=1)  # Expiry in the future
        
        token = jwt.encode(
            {"exp": expiration},
            key.key,
            algorithm="RS256",
            headers={"kid": kid}
        )
        return token
    except Exception as e:
        print(f"Error issuing JWT: {e}")
        return None

@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired') == 'true'  # Check for expired flag
    kid = "key1"  # Default to key1 or adjust logic

    if expired:
        kid = "key2"  # Use expired key if requested

    token = issue_jwt(kid, expired=expired)  # Pass expired flag to issue_jwt
    if not token:
        return jsonify({"error": "Failed to issue JWT"}), 500

    return jsonify({"token": token})

if __name__ == "__main__":
    app.run(port=8080)

#http://localhost:8080/jwks
#curl -X POST http://localhost:8080/auth in command prompt
#curl -X POST http://localhost:8080/auth?expired=true in command prompt


