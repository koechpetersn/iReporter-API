from flask_bcrypt import Bcrypt
from hashlib import sha256



print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
password_one = "pass"
password_two = "pass"
a = Bcrypt().generate_password_hash(password_one)
b = Bcrypt().generate_password_hash(password_two)
if a == b:
    print ("Same")
else:
    print("not same")


print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
c = sha256(a)
d = sha256(b)

if a == b :
    print("same")
else:
    print("not same")

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# import bcrypt
# password = b"super secret password"
# # Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
# # Check that an unhashed password matches one that has previously been
# # hashed
# if bcrypt.checkpw(password, hashed):
#     print("It Matches!")
# else:
#     print("It Does not Match :(")