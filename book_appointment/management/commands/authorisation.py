import re
import asyncio
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from contextlib import contextmanager
from async_timeout import timeout
from django.core.management.base import BaseCommand
from book_appointment.solve_captcha import get_result_capthca
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time


URL = 'https://cgifederal.secure.force.com'
REMOTE_SERVER_URL = 'http://127.0.0.1:4444/wd/hub'

CAPTCHA_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:theId'
EMAIL_FIELD_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:username'
PASSWORD_FIELD_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:password'
PRIVACY_STATEMENT_CHECKBOX_ELEMENT_NAME = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:j_id167'
CAPTCHA_FIELD_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:recaptcha_response_field'
LOGIN_BUTTON_FIELD_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:loginButton'
AUTHORIZED_USER_ELEMENT_XPATH = '//*[@id="nav"]/ul/li[2]/span'

REGEX_SEARCH_CAPTCHA = r'data:image;base64,.'
WAITING_TIME = 10


class Command(BaseCommand):
    help = 'Parse telegram channel for fetch required info about reservation'

    def add_arguments(self, parser):
        parser.add_argument('email' , help='enter email')
        parser.add_argument('password', help='enter password')

    def handle(self,*args,**options):
        email = options['email']
        password = options['password']
        captcha_queue = asyncio.Queue()
        with start_chrome_driver() as driver:
            driver.get(URL)
            asyncio.run(pass_authorization_on_site(driver, email, password,captcha_queue))


@contextmanager
def start_chrome_driver():
    """Launches the Chrome driver.
    At the end of the work, it closes all open windows,
    exits the browser and services, and frees up all resources.
    """
    driver = webdriver.Remote(REMOTE_SERVER_URL, DesiredCapabilities.CHROME)
    try:
        yield driver
    finally:
        driver.quit()


class SearchCaptchaDataInElement():
    """Search for captcha data in an element attribute.
    Searches using a regular expression.
    """

    def __init__(self, locator, pattern):
        self.locator = locator
        self.pattern = re.compile(pattern)

    def __call__(self, driver):
        try:
            element = ec._find_element(driver, self.locator)
            element_src = element.get_attribute('src')
            return self.pattern.search(element_src)
        except StaleElementReferenceException:
            return False


async def get_captcha_base64_image(driver):
    """Get captcha image in base64 format.

    If it is not possible to find an element,
    within the timeout period, it throws a TimeoutException.
    """
    async with timeout(WAITING_TIME) as cm:
        wait = WebDriverWait(driver, WAITING_TIME)

        print(dir(driver))
        time.sleep(3)

        image_element_search_pattern = SearchCaptchaDataInElement(
                (By.ID, CAPTCHA_ELEMENT_ID),
                REGEX_SEARCH_CAPTCHA
            )
        while True:
            image_element = image_element_search_pattern(driver)
            if image_element:
                break

        _, base64_img = image_element.string.split(',')
        # while not base64_img:
        #         #     await asyncio.sleep(1)
        await asyncio.sleep(2)
        return base64_img


async def pass_authorization_on_site(driver, email, password,captcha_queue):
    """Make authorization on the site.
    Enter the necessary credentials, such as login, password
    and captcha for authorization on the site.
    """

    base64_img = await get_captcha_base64_image(driver)
    print('fetch image')
    print(base64_img)
    await get_result_capthca(captcha_queue, base64_img)

    captcha_text = await captcha_queue.get()

    email_field = driver.find_element_by_id(EMAIL_FIELD_ELEMENT_ID)
    email_field.send_keys(email)

    password_field = driver.find_element_by_id(PASSWORD_FIELD_ELEMENT_ID)
    password_field.send_keys(password)

    privacy_statement_checkbox = driver.find_element_by_name(
        PRIVACY_STATEMENT_CHECKBOX_ELEMENT_NAME
    )
    privacy_statement_checkbox.click()

    captcha_field = driver.find_element_by_id(CAPTCHA_FIELD_ELEMENT_ID)
    captcha_field.send_keys(captcha_text)

    login_button = driver.find_element_by_id(LOGIN_BUTTON_FIELD_ID)
    login_button.click()

    await asyncio.sleep(60)



