from behave import given, when, then
from selenium.webdriver.common.by import By


@given('we are on the index page')
def step_impl(context):
    context.browser.get(context.index_page)
    context.domain = None


@then('we see a website for {domain}')
def step_impl(context, domain):
    element = context.browser.find_element(By.XPATH, f"//td[@id='{domain}']")
    context.domain = domain


@then(u'we see a website on {domain} owned by {user}')
def step_impl(context, domain, user):
    raise NotImplementedError(u'STEP: Then we see a website on test.example.org owned by system')


