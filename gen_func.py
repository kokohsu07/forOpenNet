import time
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from random import randrange
from variable import *
from config import *


@pytest.fixture(name="mobile")
def mobile_fixture() -> Chrome:
    mobile_emulation = {"deviceName": mobile_device}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option("windowTypes", ["webview"])
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    mobile = webdriver.Chrome(options=chrome_options)
    mobile.get(url)
    yield mobile
    mobile.quit()

def click_element(method,value,driver):
    element = wait_element_present(method,value,driver)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)

def input_text(method,value,text,driver):
    element = wait_element_present(method,value,driver)
    element.send_keys(text)


def click_random_item(ele_list, driver):
    elements = wait_elements_present(XPATH, ele_list, driver)
    random_item=randrange(len(elements))
    if elements:
        ele_ran=elements[random_item]
        driver.execute_script("arguments[0].scrollIntoView();", ele_ran)
        driver.execute_script("arguments[0].click();", ele_ran)
        print(f"Clicked on the {random_item} video.")
    else:
        print("No video elements found.")

def check_video_is_playing(ele_video, driver):
    video_element = wait_element_present(XPATH, ele_video, driver)

    def is_video_playing(driver, video_element):
        return driver.execute_script(f'return !arguments[0].paused && arguments[0].currentTime > {playing_time};', video_element)

    WebDriverWait(driver, timeout).until(lambda driver: is_video_playing(driver, video_element))

def check_profile_page(driver):
    try:
        wait_element_present(XPATH,'//div[@class="Layout-sc-1xcs6mc-0 dXKWzq tw-tabs"]', driver)
        return True
    except:
        return False

def search_target_item(target_item, driver):
    click_element(XPATH, icon_search, driver)
    input_text(XPATH, input_search_bar, target_item['target_text'], driver)
    click_element(XPATH, target_item['img_target'], driver)

# def scroll_down(driver):
#     for scroll_count in range(2):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(pause_time)

def scroll_down_transform(times, offset, driver):
    for i in range(1,times):
        driver.execute_script(f"document.body.style.transform = 'translateY(-{offset}px)';")
        time.sleep(pause_time)  # Wait for the content to load
    driver.execute_script("document.body.style.transform = 'translateY(0px)';")

def wait_element_present(method,value,driver):
    if method == 'xpath':
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, value)))
    elif method == 'id':
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, value)))
    elif method == 'css':
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))

    return element

def wait_elements_present(method,value,driver):
    if method == 'xpath':
        element = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, value)))
    elif method == 'id':
        element = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.ID, value)))
    elif method == 'css':
        element = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, value)))

    return element


def take_screenshot(driver,filename):
    driver.save_screenshot('./screenshots/'+ filename + '.png')

