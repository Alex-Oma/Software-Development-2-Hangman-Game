from backend.app.core import security

p = 'a' * 200
h = security.get_password_hash(p)
print('HASH OK, length:', len(h))
print('HASH PREVIEW:', h[:60])
print('VERIFY:', security.verify_password(p, h))

