from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdxX-dBpv3rELMDnqd7pCtHEx0kSSkDzQoVVMZ971RXYSZflQ/viewform?usp=sf_link")

Accept_Language = "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7"
Accept_Encoding = "gzip, deflate"
Accept_Charset = "Accept-Charset: utf-8"

URL = "https://www.texasrealestatesource.com/dallas-tx-new-listings/"

headers = {

    "Accept-Language": Accept_Language,
    "Accept_Encoding": Accept_Encoding,
    "Accept_Charset": Accept_Charset,

}

response = requests.get(URL, headers=headers)
zillow = response.content
soup = BeautifulSoup(zillow, "lxml")

links = []
list_of_properties = soup.select(".si-listing")
for i in list_of_properties:
    link = i.get("data-url")
    links.append(f"https://www.texasrealestatesource.com{link}")

prices = [(price.getText().split()[0]) for price in soup.find_all(class_="si-listing__photo-price")]

addresses = []
list_of_addresses = soup.select(".si-listing__title")

for i in list_of_addresses:
    address_main = i.select(".si-listing__title-main")[0].getText()
    address_description = i.select(".si-listing__title-description")[0].getText()
    addresses.append(address_main + ", " + address_description)

for n in range(len(links)):
    address_of_property = driver.find_element(By.CSS_SELECTOR,
                                              "body.D8bnZd:nth-child(2) div.Uc2NEf:nth-child(8) div.teQAzf "
                                              "div.RH5hzf.RLS9Fe:nth-child(2) div.lrKTG div.o3Dpx:nth-child(2) "
                                              "div.Qr7Oae:nth-child(1) div.geS5n div.AgroKb "
                                              "div.rFrNMe.k3kHxc.RdH0ib.yqQS1.zKHdkd div.aCsJod.oJeWuf "
                                              "div.aXBtI.Wic03c div.Xb9hP > input.whsOnd.zHQkBf")

    address_of_property.send_keys(addresses[n])
    price_per_month = driver.find_element(By.CSS_SELECTOR,
                                          "body.D8bnZd:nth-child(2) div.Uc2NEf:nth-child(8) div.teQAzf "
                                          "div.RH5hzf.RLS9Fe:nth-child(2) div.lrKTG div.o3Dpx:nth-child(2) "
                                          "div.Qr7Oae:nth-child(2) div.geS5n div.AgroKb "
                                          "div.rFrNMe.k3kHxc.RdH0ib.yqQS1.zKHdkd div.aCsJod.oJeWuf div.aXBtI.Wic03c "
                                          "div.Xb9hP > input.whsOnd.zHQkBf")

    price_per_month.send_keys(prices[n])
    link_to_property = driver.find_element(By.CSS_SELECTOR,
                                           "body.D8bnZd:nth-child(2) div.Uc2NEf:nth-child(8) div.teQAzf "
                                           "div.RH5hzf.RLS9Fe:nth-child(2) div.lrKTG div.o3Dpx:nth-child(2) "
                                           "div.Qr7Oae:nth-child(3) div.geS5n div.AgroKb "
                                           "div.rFrNMe.k3kHxc.RdH0ib.yqQS1.zKHdkd div.aCsJod.oJeWuf div.aXBtI.Wic03c "
                                           "div.Xb9hP > input.whsOnd.zHQkBf")

    link_to_property.send_keys(links[n])
    submit_button = driver.find_element(By.XPATH, "//span[contains(text(),'Submit')]")
    submit_button.click()
    submit_another_response = driver.find_element(By.XPATH, "//a[contains(text(),'Submit another response')]").click()
    time.sleep(1)


driver.quit()





