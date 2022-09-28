"""Browser fixture setup and teardown

see https://behave.readthedocs.io/en/latest/practical_tips.html#selenium-example
"""
import  sys
import os

HERE = os.path.dirname(__file__ or ".")
sys.path.append(os.path.join(HERE, ".."))

from behave import fixture, use_fixture
from selenium.webdriver import Firefox
from dynamic_website_reverse_proxy.app import App
from dynamic_website_reverse_proxy.config import Config
from bottle import WSGIRefServer, default_app
from wsgiref import simple_server
import threading
from selenium.webdriver import FirefoxOptions
import tempfile
from selenium.webdriver.common.by import By
import shutil
from behave.log_capture import capture


SCREENSHOT_LOCATION = "/tmp/dyntest/screenshots"


def save_screenshot(driver, path) -> None:
    # Ref: https://stackoverflow.com/a/52572919/
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    # driver.save_screenshot(path)  # has scrollbar
    driver.find_element(By.TAG_NAME, 'body').screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size['width'], original_size['height'])
    print(f"saved screenshot at {path}")


@fixture
def browser_firefox(context):
    # -- BEHAVE-FIXTURE: Similar to @contextlib.contextmanager
    # run firefox in headless mode
    # see https://stackoverflow.com/a/47642457/1320237
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    context.browser = browser = Firefox(options=opts)
    browser.set_page_load_timeout(10)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


@fixture
def app_client(context, port=8000):
    """Add the application.

    see https://behave.readthedocs.io/en/latest/usecase_flask.html#integration-example
    """
    class MyWSGIServer(simple_server.WSGIServer):
        """Saving all my instances so I can shut them down."""
        instance = None
        def __init__(self, *args, **kw):
            self.__class__.instance = self
            super().__init__(*args, **kw)
            
        
    with tempfile.TemporaryDirectory(prefix="dyn-tests") as td:
        context.app_config = config = Config({
            "NGINX_CONF": os.path.join(td, "nginx.conf"),
            "DOMAIN": "example.com",
            "DATABASE": os.path.join(td, "db.pickle"),
            "NETWORK": "172.16.0.0/16",
            "PORT": port
        })
        context.app = app = App(config)
        bottle_app = default_app()
        app.serve_from(bottle_app)
        bserver = WSGIRefServer(port=port, server_class=MyWSGIServer)
        context.thread = threading.Thread(target=lambda: bserver.run(bottle_app))
        context.thread.start()
        context.index_page = f"http://localhost:{port}/"
        yield app
        MyWSGIServer.instance.shutdown()
        context.thread.join()


def before_all(context):
    use_fixture(browser_firefox, context)
    use_fixture(app_client, context)
    # -- NOTE: CLEANUP-FIXTURE is called after after_all() hook.
    shutil.rmtree(SCREENSHOT_LOCATION, ignore_errors=True)
    os.makedirs(SCREENSHOT_LOCATION, exist_ok=True)

def after_step(context, step):
    # see https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls
    name = step.name
    if not getattr(context, "screenshots", 0):
        context.screenshots = 0
    context.screenshots += 1
    for letter in "/:":
        name = name.replace(letter, "")
    name = name.lower()
    name = name.replace(" ", "-")
    path = os.path.join(SCREENSHOT_LOCATION, "{0:0>2}-{1}.png".format(context.screenshots, name))
    save_screenshot(context.browser, path)