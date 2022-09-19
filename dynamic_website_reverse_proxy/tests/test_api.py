"""Test the API as used by the app.

"""
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, USER1, USER2
from unittest.mock import Mock
from http import HTTPStatus
import pytest
from .config import Config


REQUEST1 = {"domain": "test.example.com", "source": "http://10.0.0.2"}
REQUEST2 = {"domain": "21.example.com", "source": "http://10.0.0.4"}

def response_created(user, post):
    """The website was created."""
    return {
        "status": HTTPStatus.CREATED,
        "data": {
            "type": "website",
            "domain": post["domain"],
            "source": post["source"],
            "owner": user.id,
        }
    }

class TestCreateWebsite:
    """Tests to create a new website"""

    @pytest.mark.parametrize("user,post,build_response", [
        (USER1, REQUEST1, response_created),
        (ANONYMOUS, REQUEST1, response_created),
        (ADMIN, REQUEST2, response_created),
    ])
    def test_response(self, apiv1, user, post, build_response, permission_granted):
        """Test that the API delivers the correct response."""
        data = apiv1.create_website(user, post)
        assert data == build_response(user, post)

    @pytest.mark.parametrize("user,post,attribute,expected", [
        (USER1, REQUEST1, "domain", REQUEST1["domain"]),
        (USER1, REQUEST1, "source_url", REQUEST1["source"]),
        (USER1, REQUEST1, "owner", USER1),

        (ADMIN, REQUEST2, "domain", REQUEST2["domain"]),
        (ANONYMOUS, REQUEST2, "source_url", REQUEST2["source"]),

        (ADMIN, REQUEST1, "owner", ADMIN),
        (ANONYMOUS, REQUEST2, "owner", ANONYMOUS),
    ])
    def test_check_website(self, db, apiv1, user, post, attribute, expected, permission_granted):
        """Check the website that was created."""
        apiv1.create_website(user, post)
        db.add_website.assert_called_once()
        website = db.add_website.call_args.args[0]
        value = getattr(website, attribute)
        assert value == expected, f"website.{attribute}"

