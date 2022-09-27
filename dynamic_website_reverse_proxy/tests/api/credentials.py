"""The credentials that are username/password tuples.

"""
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, USER1, USER2, SYSTEM, USER3

# credentials
C_ANONYMOUS = None
C_ADMIN = ("admin", "secure")
C_USER1 = (USER1.id, USER1.test_password)
C_USER2 = (USER2.id, USER2.test_password)
