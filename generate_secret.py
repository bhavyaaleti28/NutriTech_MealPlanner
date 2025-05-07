import secrets
import base64

# Generate a 32-byte random key
secret_key = secrets.token_bytes(32)

# Convert to base64 for easier storage
secret_key_b64 = base64.b64encode(secret_key).decode('utf-8')

print("Generated JWT Secret Key:")
print(secret_key_b64)
print("\nCopy this key and paste it in your auth_server.py file as SECRET_KEY") 