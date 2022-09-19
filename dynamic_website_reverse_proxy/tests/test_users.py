"""Test the users.

"""
from dynamic_website_reverse_proxy.users import SYSTEM, ADMIN, ANONYMOUS, User
import pickle
import pytest


USER1 = User("Alice")
USER2 = User("Bob")

@pytest.mark.parametrize("user1,user2,name", [
    (USER1, USER1,     "user"),
    (USER1, USER2,     "other user"),
    (USER1, ADMIN,     "admin"),
    (USER1, SYSTEM,    "system"),
    (USER1, ANONYMOUS, "anonymous"),

    (ADMIN, USER1,     "other user"),
    (ADMIN, USER2,     "other user"),
    (ADMIN, ADMIN,     "admin"),
    (ADMIN, SYSTEM,    "system"),
    (ADMIN, ANONYMOUS, "anonymous"),

    (SYSTEM, USER1,     "other user"),
    (SYSTEM, USER2,     "other user"),
    (SYSTEM, ADMIN,     "admin"),
    (SYSTEM, SYSTEM,    "system"),
    (SYSTEM, ANONYMOUS, "anonymous"),

    (ANONYMOUS, USER1,     "other user"),
    (ANONYMOUS, USER2,     "other user"),
    (ANONYMOUS, ADMIN,     "admin"),
    (ANONYMOUS, SYSTEM,    "system"),
    (ANONYMOUS, ANONYMOUS, "anonymous"),
])
def test_user1_calls_user2_by_name(user1, user2, name):
    assert user1.calls(user2) == name


@pytest.mark.parametrize("user", [ADMIN, SYSTEM, ANONYMOUS])
def test_persistence_is_identical_for_special_users(user):
    assert pickle.loads(pickle.dumps(user)) is user


