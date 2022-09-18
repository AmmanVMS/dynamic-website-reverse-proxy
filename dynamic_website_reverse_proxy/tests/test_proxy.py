"""Tests for proxies.

"""
from dynamic_website_reverse_proxy.website import Website



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


