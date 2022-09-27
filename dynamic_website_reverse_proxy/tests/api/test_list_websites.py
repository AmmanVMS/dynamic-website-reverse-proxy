"""Test the API as used by the app.

"""
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, USER1, USER2, SYSTEM, USER3
from http import HTTPStatus
import pytest
from dynamic_website_reverse_proxy.api import InvalidUserName, InvalidLogin
from .credentials import *


class TestWebsiteList:
    """Make sure that the list of websites can be used and retrieved."""

    mark_credentials= pytest.mark.parametrize("credentials", [
        C_USER1,
        C_ADMIN,
        C_ANONYMOUS
    ])

    @mark_credentials
    def nobody_can_see_anything_if_there_are_no_websites(self, credentials, apiv1):
        """No websites, empty list."""
        websites = apiv1.list_websites(credentials)
        assert websites["status"] == 200
        assert websites["data"] == []

    @mark_credentials
    def test_nobody_can_see_a_website_if_permissions_are_not_granted(self, credentials, apiv1, added_website):
        websites = apiv1.list_websites(credentials)
        assert websites["status"] == 200
        assert websites["data"] == []

    @mark_credentials
    def test_website_is_visible_if_permission_is_granted(self, credentials, apiv1, added_website, permission_granted):
        websites = apiv1.list_websites(credentials)
        assert websites["status"] == 200
        assert websites["data"] == [added_website.to_json()]
        






        