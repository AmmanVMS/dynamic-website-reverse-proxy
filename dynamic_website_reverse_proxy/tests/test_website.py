"""Test website objects.
"""
from dynamic_website_reverse_proxy.website import Website


def test_source_is_in_config(website, source):
    assert f"proxy_pass {source};" in website.get_nginx_configuration()


def test_domain_is_used(website, domain, sub_domain):
    assert f"server_name {sub_domain + '.' + domain};" in website.get_nginx_configuration()


def test_http_port_is_considered(website, http_port):
    assert f"listen 0.0.0.0:{http_port};" in website.get_nginx_configuration()


def test_domain_attibute(website, domain, sub_domain):
    assert website.domain == f"{sub_domain}.{domain}"


def test_id_is_subdomain(website, sub_domain):
    assert website.id == sub_domain


def test_identity(website):
    """Test equality."""
    assert website == website
    assert hash(website) == hash(website)


def test_equality(website, sub_domain, config, source):
    """Test equality."""
    other_website = Website(source, sub_domain, config)
    assert website == other_website
    assert hash(website) == hash(other_website)

def test_inequality(website, config, source):
    """Test equality."""
    other_website = Website(source, "other-subdomain", config)
    assert website != other_website
    assert hash(website) != hash(other_website)


