# # from cryptography.hazmat.primitives import hashes
# # from cryptography.hazmat.primitives.asymmetric import padding
# # import cryptography
# # from cryptography.hazmat.backends import default_backend
# # from cryptography.hazmat.primitives.asymmetric import rsa
# # from cryptography.hazmat.primitives import serialization


# # private_key = rsa.generate_private_key(
# #     public_exponent=65537,
# #     key_size=2048,
# #     backend=default_backend()
# # )
# # public_key = private_key.public_key()

# # # private key
# # serial_private = private_key.private_bytes(
# #     encoding=serialization.Encoding.PEM,
# #     format=serialization.PrivateFormat.PKCS8,
# #     encryption_algorithm=serialization.NoEncryption()
# # )
# # # print(serial_private)

# # # public key
# # serial_pub = public_key.public_bytes(
# #     encoding=serialization.Encoding.PEM,
# #     format=serialization.PublicFormat.SubjectPublicKeyInfo
# # )

# # # print(serial_pub)


# # # make sure the following are imported
# # # from cryptography.hazmat.backends import default_backend
# # # from cryptography.hazmat.primitives import serialization
# # #########      Private device only    ##########
# # read_private_key = serialization.load_pem_private_key(
# #     serial_private,
# #     password=None,
# #     backend=default_backend()
# # )


# # read_public_key = serialization.load_pem_public_key(
# #     serial_pub,
# #     backend=default_backend()
# # )

# # # print(public_key)
# # # print(type(serial_pub.decode('utf-8')))
# # # print(read_public_key)


# # data = b'My secret weight'

# # encrypted = public_key.encrypt(
# #     data,
# #     padding.OAEP(
# #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
# #         algorithm=hashes.SHA256(),
# #         label=None
# #     )
# # )


# # #########      DECRYPTING WITH PRIVATE KEY    ##########
# # private_key.decrypt(
# #     encrypted,
# #     padding.OAEP(
# #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
# #         algorithm=hashes.SHA256(),
# #         label=None
# #     ))


# import hmac
# from cryptography.fernet import Fernet
# from builtins import bytes
# import hashlib
# from os import urandom
# from base64 import b64encode
# import os


# byte_key = os.urandom(16)
# print(byte_key)
# hexed_byte_key = byte_key.hex()
# print(hexed_byte_key)
# print(type(hexed_byte_key))
# recovered_byte_key = bytes.fromhex(hexed_byte_key)
# print(recovered_byte_key)

# # encoded_key = hashlib.shake_256(key.encode()).digest(16)
# # print(encoded_key)
# # decoded_key = bytes.fromhex(encoded_key)
# # print(decoded_key)

# # print(hashlib.shake_256(key.encode()).hexdigest(16))
# # key = hashlib.sha256(key.encode()).hexdigest()
# # random_bytes = urandom(64)
# # token = b64encode(random_bytes).decode('utf-8')
# # print(bytes.fromhex(key).decode('utf-8'))
# # # print(token)
# # mykey = os.urandom(16)
# # b',Ca8\xcc}\x1b\x8a\x8f_\xe6\xac\xa7\x93\xa6K'

# key = Fernet.generate_key()
# print(key)


# nonce = 1
# customer_id = 123456
# API_SECRET = 'thekey'
# api_key = 'thapikey'

# message = '{} {} {}'.format(nonce, customer_id, api_key)

# signature = hmac.new(bytes(API_SECRET, 'latin-1'), msg=bytes(message,
#                      'latin-1'), digestmod=hashlib.sha256).hexdigest().upper()
# print(signature)
from passlib.hash import pbkdf2_sha256
# import pyaes
# import pbkdf2
# import binascii
# import os
# import secrets

# # Derive a 256-bit AES encryption key from the password
# password = "s3cr3t*c0d3"
# passwordSalt = os.urandom(16)
# # print(passwordSalt)

# key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
# # print('AES encryption key:', key)
# # print('AES encryption key:', binascii.hexlify(key))
# # print('AES encryption key:', key.hex())


# # Encrypt the plaintext with the given key:
# #   ciphertext = AES-256-CTR-Encrypt(plaintext, key, iv)
# iv = secrets.randbits(256)
# print(iv)
# plaintext = "Text for encryption"
# aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))

# ciphertext = aes.encrypt(plaintext)
# print('Encrypted:', binascii.hexlify(ciphertext))
import secrets
key = secrets.token_urlsafe(16)
print(key)
hash = pbkdf2_sha256.hash("asimnepal")
print(hash)
print(pbkdf2_sha256.verify("password", hash))
print(pbkdf2_sha256.verify("asimnepal", hash))
print(len(hash))
