import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities

from scraping_flights.config import FIREFOX_BINARY_LOCATION
from selenium import webdriver


def start_browser(url, headless=False) -> webdriver:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    options.add_argument("--window-size=1920,1080")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", get_useragent())
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.accept_untrusted_certs = True
    options.binary_location = FIREFOX_BINARY_LOCATION
    # driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)
    driver.get(url)
    # driver.delete_all_cookies()
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.execute_script("window.focus();")
    driver.maximize_window()
    return driver


#

# def start_browser(url):
#     options = uc.ChromeOptions()
#     caps = DesiredCapabilities().CHROME
#     caps["pageLoadStrategy"] = "eager"
#     # options.add_argument(f"user-agent={get_useragent()}")
#     # options.add_argument("user-data-dir=selenium")
#     options.add_argument("window-size=1920,1080")
#     options.add_argument("--start-maximized")
#     options.add_argument("--headless")
#     driver = uc.Chrome(options=options, desired_capabilities=caps)
#     driver.get(url)
#     return driver


def chrome_options():
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    return options


def get_useragent():
    ua = UserAgent()
    user_agent = ua.firefox
    return user_agent


if __name__ == "__main__":
    driver = uc.Chrome()
    driver.get("https://www.google.com/")
