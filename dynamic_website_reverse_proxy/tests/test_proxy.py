"""Tests for proxies.

"""
from dynamic_website_reverse_proxy.website import Website
from dynamic_website_reverse_proxy.users import ANONYMOUS, ADMIN, USER1, USER2, SYSTEM, UniqueUser
import pytest


def test_initial_proxy_has_no_entries(proxy):
    assert len(proxy.websites) == 0


def test_add_website(proxy, website):
    proxy.add(website)
    assert len(proxy.websites) == 1
    assert proxy.websites[0] == website


def test_add_website_twice_does_nothing(proxy, website):
    proxy.add(website)
    proxy.add(website)
    assert len(proxy.websites) == 1
    assert proxy.websites[0] == website


def test_proxy_includes_website_configuration_if_added(proxy, website):
    proxy.add(website)
    assert website.get_nginx_configuration() in proxy.get_nginx_configuration()


def test_proxy_includes_no_website_configuration(proxy, website):
    assert website.get_nginx_configuration() not in proxy.get_nginx_configuration()


def test_entries_with_same_domain_name_are_replaced_if_source_differs(proxy, website, sub_domain, config, source):
    proxy.add(website)
    website2 = Website("http://replaced-source.com", sub_domain, config)
    proxy.add(website2)
    assert website not in proxy.websites
    assert website2 in proxy.websites


def test_entries_with_different_domain_name_are_not_replaced(proxy, website, sub_domain, config, source):
    proxy.add(website)
    website2 = Website(source, "other-subdomain", config)
    proxy.add(website2)
    assert website in proxy.websites
    assert website2 in proxy.websites


def test_reloading_config_does_nothing(proxy, config):
    proxy.reload(config)
    assert len(proxy.websites) == 0


def test_website_loaded_by_config_is_added(proxy, config, website):
    proxy.reload(config.new(websites=[website]))
    assert website in proxy.websites


def test_website_loaded_by_config_is_not_added_twice(proxy, config, website):
    proxy.reload(config.new(websites=[website]))
    proxy.reload(config.new(websites=[website]))
    assert len(proxy.websites) == 1


def test_different_domain_name_in_website_adds_it(proxy, website, sub_domain, config, source):
    proxy.add(website)
    website2 = Website(source, "other-subdomain", config)
    proxy.reload(config.new(websites=[website2]))
    assert len(proxy.websites) == 2
    assert website in proxy.websites   
    assert website2 in proxy.websites   


def test_website_from_config_has_precedence(proxy, website, sub_domain, config):
    proxy.add(website)
    website2 = Website("http://alternative-source.py", sub_domain, config)
    proxy.reload(config.new(websites=[website2]))
    assert len(proxy.websites) == 1
    assert website not in proxy.websites   
    assert website2 in proxy.websites   


def test_proxy_with_no_websites_cannot_get_a_website(proxy, website):
    assert proxy.get(website.id) == None


def test_proxy_get_non_existent_website(proxy, website):
    proxy.add(website)
    assert proxy.get(website.id + "asd") == None


def test_proxy_get_existent_website(proxy, website):
    proxy.add(website)
    assert proxy.get(website.id) == website


class TestUsers:
    """Tests for proxy.users"""

    def test_proxy_has_no_users_at_start(self, proxy):
        assert len(proxy.users) == 0

    @pytest.mark.parametrize("user", [USER1, USER2])
    def test_proxy_collects_users_from_websites(self, proxy, website, user):
        proxy.add(website)
        website.change_owner_to(user)
        assert user in proxy.users
        assert len(proxy.users) == 1

    @pytest.mark.parametrize("user", [SYSTEM, ANONYMOUS, ADMIN, UniqueUser("unique test user", "unique test user", "unique test user")])
    def test_proxy_does_not_collect_unique_users(self, proxy, website, user):
        proxy.add(website)
        website.change_owner_to(user)
        assert len(proxy.users) == 0
