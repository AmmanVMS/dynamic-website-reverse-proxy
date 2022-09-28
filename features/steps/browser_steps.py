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
    context.website = element


@then('the website\'s {attribute} is "{value}"')
def step_impl(context, attribute, value):
    assert getattr(context, "website", None) is not None, "Error in the order of the steps: there should be a 'we see a website for ...' step before this one!"
    element = context.website.find_element(By.XPATH, f"//*[@class='{attribute}']")
    assert element.text == value, f"The text in {element} should be '{value}' and not '{element.text}'."

