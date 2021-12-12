import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)
driver.get('https://www.nintendo.co.jp/software/campaign/index.html')

soft_name_list = []
while True:
    for element in driver.find_elements_by_class_name("nc3-c-softCard__name"):
        soft_name_list.append(element.text)
    try:
        next_page = driver.find_element_by_class_name("nc3-c-pagination__next")
        next_page.click()
        time.sleep(3)
    except ElementNotInteractableException:
        driver.quit()
        break
