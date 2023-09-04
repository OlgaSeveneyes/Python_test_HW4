from testpage import OperationHelper
import logging
import time
import requests
import yaml

with open("testdata.yaml") as f:
    data = yaml.safe_load(f)
    name = data["username"]
    passwd = data["password"]
    test = data["test"]
    url_token = data["url_get_token"]
    url_api_posts = data["url_api_posts"]

def login_check(user, passwd, url, block):
    obj_data = requests.post(url=url,
                             data={'username': f'{user}',
                                   'password': f'{passwd}'})
    check_login = obj_data.json()[f'{block}']
    # print('\ncheck_login - ', check_login)

    return str(check_login)

def token_auth(token, url, block):
    res = requests.get(url=url,
                       headers={"X-Auth-Token": token},
                       params={"owner": "Me"})
    content = [item[f"{block}"] for item in res.json()['data']]
    # print('\ncontent - ', content)
    return content

def test_step1(browser):
    logging.info("Test1 Starting")
    testpage = OperationHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(test)
    testpage.enter_pass(test)
    testpage.click_login_button()
    time.sleep(3)
    assert "401" in login_check(test, test, url_token, 'code'), "Test_1 FAIL"

def test_step2(browser):
    logging.info("Test2 Starting")
    testpage = OperationHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(name)
    testpage.enter_pass(passwd)
    testpage.click_login_button()
    time.sleep(2)
    assert f"{name}" in login_check(name, passwd, url_token, 'username'), "Test_2 FAIL"

def test_step3(browser, login):
    logging.info("Test3 Starting")
    testpage = OperationHelper(browser)
    testpage.click_to_do_new_post()
    testpage.enter_title("Field_title")
    testpage.enter_description("Field_description")
    testpage.enter_content("Field_content")
    testpage.click_save_post_button()
    time.sleep(5)
    token_auth(login, url_api_posts, 'title')
    assert "Field_title" in token_auth(login, url_api_posts, 'title'), "Test_3 FAIL"

def test_step4(browser, login):
    logging.info("Test4 Starting")
    testpage = OperationHelper(browser)
    testpage.click_contact_button()
    testpage.enter_name("Field_name")
    testpage.enter_email("email@gmail.ru")
    testpage.enter_contact_content("field_contact_content")
    testpage.contact_us_save_button()
    time.sleep(3)
    alert = testpage.get_alert_text()
    assert alert == "Form successfully submitted", "Test_4 FAIL"
