from behave import given, when, then
from selenium.webdriver.common.by import By

#
# Website checks
#

@given('we are on the index page')
def step_impl(context):
    context.browser.get(context.index_page)
    context.domain = None

@then('we see the title "{title}"')
def step_impl(context, title):
    assert context.browser.title == title
    return context.browser.title

@then('we see a heading "{title}"')
def step_impl(context, title):
    element = context.browser.find_element(By.XPATH, f"//*[text()='{title}' and (self::h1 or self::h2 or self::h3 or self::h4 or self::h5)]")
    print(dir(element))
    assert element.tag_name in "h1 h2 h3 h4 h5", f"{element.tag_name} should be a heading."
    return element

#
# Checks for proxy entries
#

@then('we see a website for {domain}')
def step_impl(context, domain):
    element = context.browser.find_element(By.XPATH, f"//tr[@id='{domain}']")
    context.domain = domain



@then(u'we see a website on {domain} owned by {user}')
def step_impl(context, domain, user):
    raise NotImplementedError(u'STEP: Then we see a website on test.example.org owned by system')

