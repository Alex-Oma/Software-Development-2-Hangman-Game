# A simple script to test password hashing and verification
from backend.app.core import security

# Test password hashing and verification
p = 'a' * 200
# Generate hash
h = security.get_password_hash(p)
print('HASH OK, length:', len(h))
print('HASH PREVIEW:', h[:60])
# Verify password
print('VERIFY:', security.verify_password(p, h))

