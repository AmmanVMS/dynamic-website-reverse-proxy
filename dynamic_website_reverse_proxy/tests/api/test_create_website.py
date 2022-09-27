"""Test the API as used by the app.

"""
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, USER1, USER2, SYSTEM, USER3
from unittest.mock import Mock
from http import HTTPStatus
import pytest
from ..config import Config
from .credentials import *


REQUEST1 = {"domain": "test.example.com", "source": "http://10.0.0.2"}
REQUEST2 = {"domain": "meine-webseite.quelltext.eu", "source": "http://10.0.0.4"}

def response_created(user, post):
    """The website was created."""
    return {
        "status": HTTPStatus.CREATED,
        "data": {
            "type": "website",
            "domain": post["domain"],
            "source": post["source"],
            "owner": (user[0] if user else ANONYMOUS.id),
        }
    }

# credentials
C_ANONYMOUS = None
C_ADMIN = ("admin", "secure")
C_USER1 = (USER1.id, USER1.test_password)
C_USER2 = (USER2.id, USER2.test_password)

class TestCreateWebsite:
    """Tests to create a new website"""

    @pytest.mark.parametrize("user,post,build_response", [
        (C_USER1, REQUEST1, response_created),
        (C_ANONYMOUS, REQUEST1, response_created),
        (C_ADMIN, REQUEST2, response_created),
    ])
    def test_response(self, apiv1, user, post, build_response, permission_granted):
        """Test that the API delivers the correct response."""
        data = apiv1.create_website(user, post)
        assert data == build_response(user, post)

    @pytest.mark.parametrize("user,post,attribute,expected", [
        (C_USER1, REQUEST1, "domain", REQUEST1["domain"]),
        (C_USER1, REQUEST1, "source_url", REQUEST1["source"]),
        (C_USER1, REQUEST1, "owner", USER1),

        (C_ADMIN, REQUEST2, "domain", REQUEST2["domain"]),
        (C_ANONYMOUS, REQUEST2, "source_url", REQUEST2["source"]),

        (C_ADMIN, REQUEST1, "owner", ADMIN),
        (C_ANONYMOUS, REQUEST2, "owner", ANONYMOUS),
    ])
    def test_check_website(self, db, apiv1, user, post, attribute, expected, permission_granted):
        """Check the website that was created."""
        print(apiv1.create_website(user, post))
        db.proxy.add.assert_called_once()
        website = db.proxy.add.call_args.args[0]
        value = getattr(website, attribute)
        assert value == expected, f"website.{attribute}"

    @pytest.mark.parametrize("any_user", [C_USER1, C_USER2, C_ANONYMOUS, C_ADMIN])
    @pytest.mark.parametrize("post,message", [
        ({}, "The field 'domain' is missing."),
        ({"domain": ""}, "The field 'source' is missing."),
        ({"domain": "", "source": "http://10.0.0.4"}, "The field 'domain' must be a valid domain name."),
        ({"domain": " asd", "source": "http://10.0.0.4"}, "The field 'domain' must be a valid domain name."),
        ({"domain": ".asd", "source": "http://10.0.0.4"}, "The field 'domain' must be a valid domain name."),
        ({"domain": "test.example.com", "source": "http10.0.0.4"}, "The field 'source' must be a valid http/https url."),
        ({"domain": "test.example.com", "source": "ftp://10.0.0.4"}, "The field 'source' must be a valid http/https url."),
        ({"domain": "test.example.com", "source": "https://10.0.100.4"}, "The field 'source' must be inside 10.0.0.0/24."),
    ])
    def test_fields_missing(self, apiv1, any_user, post, message):
        """Check error message of invalid fields."""
        response = apiv1.create_website(any_user, post)
        assert response["status"] == HTTPStatus.BAD_REQUEST, message
        assert response["error"]["message"] == message

    no_permission = pytest.mark.parametrize("user,post,message", [
        (C_ADMIN, REQUEST1, "admin cannot create subdomain owned by admin"),
        (C_USER1, REQUEST2, "user cannot create fqdn owned by user"),
    ])

    @no_permission
    def test_permission_denied(self, apiv1, user, message, post):
        response = apiv1.create_website(user, post)
        assert response["status"] == HTTPStatus.UNAUTHORIZED, message
        assert response["error"]["message"] == message
    
    @no_permission
    def test_action_tested(self, apiv1, user, message, post, permissions):
        response = apiv1.create_website(user, post)
        assert len(permissions.actions) > 0, "Someone should ask for permission!"
        denied_message = message.replace("cannot", "can")
        assert denied_message in permissions.actions
    
    @no_permission
    def test_website_not_added(self, db, apiv1, user, post, message):
        """The website is not added if no permission is given."""
        apiv1.create_website(user, post)
        db.proxy.add.assert_not_called()
