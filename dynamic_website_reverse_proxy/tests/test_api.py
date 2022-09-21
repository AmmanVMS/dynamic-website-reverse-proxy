"""Test the API as used by the app.

"""
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, USER1, USER2, SYSTEM, USER3
from unittest.mock import Mock
from http import HTTPStatus
import pytest
from .config import Config
from dynamic_website_reverse_proxy.api import InvalidUserName, InvalidLogin


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
        (ADMIN, REQUEST1, "admin cannot create subdomain owned by admin"),
        (USER1, REQUEST2, "user cannot create fqdn owned by user"),
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
        db.add_website.assert_not_called()


class TestUserIdentification:
    """A set of tests that make sure that the user is correctly identified."""
    
    def test_anonymous(self, apiv1):
        """None is the anonymous user."""
        assert apiv1.login(None) == ANONYMOUS

    def test_system_raises_an_error(self, apiv1):
        """system cannnot be logged in."""
        with pytest.raises(InvalidUserName):
            apiv1.login((SYSTEM.id, ""))

    def test_invalid_user_name_http_status(self):
        error = InvalidUserName("")
        assert error.http_status == HTTPStatus.NOT_ACCEPTABLE

    def test_invalid_login_http_status(self):
        error = InvalidLogin("")
        assert error.http_status == HTTPStatus.UNAUTHORIZED

    @pytest.mark.parametrize("name", ["Alice", "system"])
    def test_invalid_user_name_message(self, name):
        error = InvalidUserName(name)
        assert str(error) == f"You can not use the name '{name}' on this system."

    @pytest.mark.parametrize("user", [ADMIN, USER1])
    @pytest.mark.parametrize("password", ["asd", "jshdkjfhkjsdhfkjhskjdhfjhksjdhfjskd"])
    def test_login_admin(self, apiv1, apiv1_config, user, password):
        """The admin user can login with a password.

        The admin password can be used by any user to log in so that the admin
        can impersonate other users to change their password.
        """
        apiv1_config.update(admin_password=password)
        logged_in_user = apiv1.login((user.id, password))
        assert logged_in_user == user, f"{user.name} with password {password}"
        
    @pytest.mark.parametrize("user", [USER1, USER2])
    def test_login_user(self, apiv1, user):
        """Successful login."""
        assert apiv1.login((user.id, user.test_password)) == user

    @pytest.mark.parametrize("username,password", [
        (USER1.id, USER1.test_password + " "), # wrong password
        (USER2.id, ""), # empty admin password
        (ADMIN.id, ""), # empty admin password
        (ADMIN.id, "asdasd"), # wrong password
        (USER3.id, USER3.test_password), # not in database
        ("    ", ""), # totally wrong
    ])
    def test_login_fails(self, apiv1, username, password, apiv1_config):
        """Certain logins should not work."""
        apiv1_config.update(admin_password=password * 2)
        with pytest.raises(InvalidLogin):
            apiv1.login((username, password))
                















        