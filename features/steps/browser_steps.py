from behave import given, when, then
from selenium.webdriver.common.by import By

#
# Website checks
#

@given('we are on the index page')
def visit_index_page(context):
    context.browser.delete_all_cookies()
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

XPATH_TAG_WITH_TYPE_AND_NAME = "//{tag}[@type='{type}' and @name='{name}']"

@then('we see a {type} {tag} for the {name}')
def step_impl(context, type, tag, name):
    """Find an element of the description."""
    # @type from https://stackoverflow.com/a/24370382/1320237
    element = context.browser.find_element(By.XPATH, XPATH_TAG_WITH_TYPE_AND_NAME.format(tag=tag, type=type, name=name))

@then('we see "{text}" in the {type} {tag} for the {name}')
def step_impl(context, text, type, tag, name):
    """Find an element of the description."""
    # @type from https://stackoverflow.com/a/24370382/1320237
    element = context.browser.find_element(By.XPATH, XPATH_TAG_WITH_TYPE_AND_NAME.format(tag=tag, type=type, name=name))
    value = element.get_attribute("value")
    assert value == text, f"Expected {element}.value to be '{text}' but it is '{value}'."

@then('we do not see a {type} {tag} for the {name}')
def step_impl(context, type, tag, name):
    """Find no elements of the description."""
    # @type from https://stackoverflow.com/a/24370382/1320237
    elements = context.browser.find_elements(By.XPATH, XPATH_TAG_WITH_TYPE_AND_NAME.format(tag=tag, type=type, name=name))
    assert len(elements) == 0, f"There should not be any element but there are {elements}."

XPATH_BUTTON_WITH_TEXT = "//input[(@type='button' or @type='submit') and @value='{text}']"

@then('we see a button "{text}"')
def step_impl(context, text):
    """There is a button."""
    # @type from https://stackoverflow.com/a/24370382/1320237
    element = context.browser.find_element(By.XPATH, XPATH_BUTTON_WITH_TEXT.format(text=text))

@then('we do not see a button "{text}"')
def step_impl(context, text):  
    """There is a button."""
    # @type from https://stackoverflow.com/a/24370382/1320237
    elements = context.browser.find_elements(By.XPATH, XPATH_BUTTON_WITH_TEXT.format(text=text))
    assert len(elements) == 0, f"There should not be a button with '{text}' on it but there is: {elements}."


#
# Website interaction
#

@when('we click "{text}"')
def click(context, text):
    element = context.browser.find_element(By.XPATH, f"//*[(self::a and text()='{text}') or (self::input and @value='{text}')]")
    element.click()

@when('we click "{text}" in {id}')
def click_in(context, text, id):
    """Click a link or button inside of another element."""
    element = context.browser.find_element(By.XPATH, f"//*[@id='{id}']//*[(self::a and text()='{text}') or (self::input and @value='{text}')]")
    element.click()


@then('we type "{text}" into the {tag} for the {name}')
def type_in(context, text, tag, name):
    element = context.browser.find_element(By.XPATH, f"//{tag}[@name='{name}']")
    element.send_keys(text)

#
# Checks for proxy entries
#

@then('we see a website for {domain}')
def step_impl(context, domain):
    element = context.browser.find_element(By.XPATH, f"//tr[@id='{domain}']")
    context.domain = domain
    

@then('the website\'s {attribute} is "{value}"')
def step_impl(context, attribute, value):
    assert getattr(context, "domain", None) is not None, "Error in the order of the steps: there should be a 'we see a website for ...' step before this one!"
    element = context.browser.find_element(By.XPATH, f"//tr[@id='{context.domain}']//*[@class='{attribute}']")
    assert element.text == value, f"The text in {element} should be '{value}' and not '{element.text}'."

#
# Login steps
#

@then('we see a {id} notice "{notice}"')
def notice_says(context, id, notice):
    element = context.browser.find_element(By.XPATH, f"//*[@id='{id}-notice']")
    assert element.text == notice, f"I expect element .{id}-notice to have the text '{notice}' but its text is '{element.text}'"


USERS = {
    "user": "password",
    "user2": "other-password",
    "admin": "12345" # environment.py
}

@When("we log in as {username}")
@Given("we are logged in as {username}")
def login_user(context, username):
    visit_index_page(context)
    type_in(context, username, "input", "username")
    type_in(context, USERS[username], "input", "password")
    click(context, "Log In")
    notice_says(context, "login", f"You are logged in as {username}.")

@Given("{username}'s website {domain} is served by {source}")
def create_website(context, username, domain, source):
    login_user(context, username)
    type_in(context, domain, "input", "domain")
    type_in(context, source, "input", "source")
    click(context, "Save Website")
    click(context, "Log Out")
    
