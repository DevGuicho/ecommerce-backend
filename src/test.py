import bcrypt

passwd = bytes('secret', 'UTF-8')

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)

print(salt)
print(hashed)

print(hashed.decode('UTF-8'))
