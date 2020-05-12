from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

class flagScraper:
    def __init__(self):
        path = "chromedriver.exe"
        baseURL = "https://www.countryflags.com/en/"

        option = webdriver.ChromeOptions()
        option.add_argument("--incognito")

        browser = webdriver.Chrome(path, options=option)

        browser.get(baseURL)

        timeout = 120
        try:
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='img-responsive']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        flagLinks = browser.find_elements_by_xpath("//a[@class='clearfix']")\

        urls = []
        for link in flagLinks:
            link_href = link.get_property("href")
            urls.append(link_href)

        for link in urls:
            print("Attempting to download "+link.split("/")[-1].split(".")[0])
            browser.get(link)
            try:
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='btn btn-primary btn-custom-image']")))
            except TimeoutException:
                print("Timed out waiting for page2 to load")
                browser.quit()

            imageButton = browser.find_element_by_xpath("//a[@class='btn btn-primary btn-custom-image']")
            imageButton.click()

            try:
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='btn btn-default']")))
            except TimeoutException:
                print("Timed out waiting for page3 to load")
                browser.quit()

            buttons = browser.find_elements_by_xpath("//a[@class='btn btn-default']")

            for button in buttons:
                if button.get_property("href").split("/")[-1] == "flag-png-medium.png":
                    print("Downloading "+button.get_property("href").split("/")[-2]+"...")
                    button.click()
                    break
            sleep(10)

flagScraper()
