import yaml
import pytest
import requests
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

with open("testdata.yaml") as f:
    testdata = yaml.safe_load(f)
    browser1 = testdata["browser"]
    url_token = testdata["url_get_token"]
    name = testdata["username"]
    passwd = testdata["password"]

@pytest.fixture()
def login():
    obj_data = requests.post(url=url_token,
                             data={'username': f'{name}',
                                   'password': f'{passwd}'})
    # print('obj_data - ', obj_data.json())
    token = obj_data.json()['token']
    return token

@pytest.fixture(scope="session")
def browser():
    if browser1 == "firefox":
        service = Service(executable_path=GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
