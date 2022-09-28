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

@then('we see a {type} {tag} for the {name}')
def step_impl(context, type, tag, name):
    """Find an element of the description."""
    # @type from https://stackoverflow.com/a/24370382/1320237
    element = context.browser.find_element(By.XPATH, f"//{tag}[@type='{type}' and @name='{name}']")

#
# Website interaction
#

@then('we click "{text}"')
def step_impl(context, text):
    element = context.browser.find_element(By.XPATH, f"//*[(self::a and text()='{text}') or (self::input and @value='{text}')]")
    element.click()

@then('we type "{text}" into the {tag} for the {name}')
def step_impl(context, text, tag, name):
    element = context.browser.find_element(By.XPATH, f"//{tag}[@name='{name}']")
    element.send_keys(text)

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

#
# Login steps
#

@then('we see a {id} notice "{notice}"')
def step_impl(context, id, notice):
    element = context.browser.find_element(By.XPATH, f"//*[@id='{id}-notice']")
    assert element.text == notice, f"I expect element .{id}-notice to have the text '{notice}' but its text is '{element.text}'"



