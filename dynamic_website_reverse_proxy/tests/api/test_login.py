"""Test the API as used by the app.

"""
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, USER1, USER2, SYSTEM, USER3
from http import HTTPStatus
import pytest
from .credentials import C_ANONYMOUS
from dynamic_website_reverse_proxy.api import InvalidUserName, InvalidLogin



class TestUserIdentification:
    """A set of tests that make sure that the user is correctly identified."""
    
    def test_anonymous(self, apiv1_obj):
        """None is the anonymous user."""
        assert apiv1_obj.login(C_ANONYMOUS) == ANONYMOUS

    def test_system_raises_an_error(self, apiv1_obj):
        """system cannnot be logged in."""
        with pytest.raises(InvalidUserName):
            apiv1_obj.login((SYSTEM.id, ""))

    def test_invalid_user_name_http_status(self):
        error = InvalidUserName("")
        assert error.http_status == HTTPStatus.NOT_ACCEPTABLE

    def test_invalid_login_http_status(self):
        error = InvalidLogin()
        assert error.http_status == HTTPStatus.UNAUTHORIZED

    @pytest.mark.parametrize("name", ["Alice", "system"])
    def test_invalid_user_name_message(self, name):
        error = InvalidUserName(name)
        assert str(error) == f"You can not use the name '{name}' on this system."

    @pytest.mark.parametrize("user", [ADMIN, USER1])
    @pytest.mark.parametrize("password", ["asd", "jshdkjfhkjsdhfkjhskjdhfjhksjdhfjskd"])
    def test_login_admin(self, apiv1_obj, apiv1_config, user, password):
        """The admin user can login with a password.

        The admin password can be used by any user to log in so that the admin
        can impersonate other users to change their password.
        """
        apiv1_config.update(admin_password=password)
        logged_in_user = apiv1_obj.login((user.id, password))
        assert logged_in_user == user, f"{user.name} with password {password}"
        
    @pytest.mark.parametrize("user", [USER1, USER2])
    def test_login_user(self, apiv1_obj, user):
        """Successful login."""
        assert apiv1_obj.login((user.id, user.test_password)) == user

    @pytest.mark.parametrize("username,password", [
        (USER1.id, USER1.test_password + " "), # wrong password
        (USER2.id, ""), # empty password
        (USER3.id, USER1.test_password), # other user's password
    ])
    def test_login_fails_with_existing_users(self, apiv1_obj, username, password, apiv1_config, db):
        """Certain logins should not work."""
        db.proxy.users = [USER1, USER2, USER3]
        with pytest.raises(InvalidLogin):
            apiv1_obj.login((username, password))

    @pytest.mark.parametrize("username,password,Error", [
        (USER2.id, "", InvalidLogin), # empty admin password
        (ADMIN.id, "", InvalidUserName), # empty admin password
        (ADMIN.id, "asdasd", InvalidLogin), # wrong password
    ])
    def test_login_fails_with_empty_admin_password(self, apiv1_obj, Error, username, password, apiv1_config, db):
        """Certain logins should not work."""
        db.proxy.users = [USER2]
        apiv1_config.update(admin_password=password * 2)
        with pytest.raises(Error):
            apiv1_obj.login((username, password))

    @pytest.mark.parametrize("username,password", [
        ("    ", ""), # totally wrong
    ])
    def test_login_fails_with_malformed_credentials(self, apiv1_obj, username, password, apiv1_config, db):
        """Certain logins should not work."""
        with pytest.raises(InvalidUserName):
            apiv1_obj.login((username, password))



        