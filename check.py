# from flask_bcrypt import Bcrypt
# from hashlib import sha256



# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# password_one = "pass"
# password_two = "pass"
# a = Bcrypt().generate_password_hash(password_one)
# b = Bcrypt().generate_password_hash(password_two)
# if a == b:
#     print ("Same")
# else:
#     print("not same")


# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# c = sha256(a)
# d = sha256(b)

# if a == b :
#     print("same")
# else:
#     print("not same")

# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# import bcrypt
# password = b"super secret password"
# print(password)
# ser = "wewe"
# arr = bytes(ser, 'utf-8')
# print(arr)
# # Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
# # Check that an unhashed password matches one that has previously been
# # hashed
# if bcrypt.checkpw(password, hashed):
#     print("It Matches!")
# else:
#     print("It Does not Match :(")
# class Mwangi():
#     def __init__(self,name):
#         self.name = name
#     """describes mwangi"""
#     @classmethod
#     def helper(cls):
#         five = None
#         if five:
#             print ("samwel")
#             m = 10
#             return m
#         else:
#             print("Nderitu")
#             fiv = 5
#             return fiv

#     def see(self):
#         kijana_round = Mwangi.helper()
#         print (kijana_round)

# nono = Mwangi("shehe")
# nono.see()


# def greet_me(**kwargs):
#     if kwargs is not None:
#         for key, value in kwargs.items():
#             print (value)

# greet_me(id="gd")

def test_args_kwargs(comment, location,media):
    print (comment)
    print (location)
    print (media)
args = ("two", 3,5)
kwargs = {"comment": "mombay", "location": "naks","media":"town"}
test_args_kwargs(*args)