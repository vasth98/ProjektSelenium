from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
def get_smartphones_neonet(min_price):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get('https://www.neonet.pl/')
    accept = driver.find_element(By.XPATH, '//*[@id="mainContainer"]/div[1]/div[3]/div/div/div[2]/button')
    accept.click()
    search = driver.find_element(By.XPATH, '//*[@id="appHeader"]/div/div/div/form/label/input')
    search.send_keys('smartfon')
    search.send_keys(Keys.ENTER)
    time.sleep(3)
    set_price = driver.find_element(By.XPATH, '//*[@id="price_from"]')
    set_price.send_keys('3000')
    set_price.send_keys(Keys.ENTER)
    time.sleep(10)

    smartphones = []
    while True:
        try:
            products = driver.find_elements(By.XPATH, '//h2[contains(@class, "3gj")]')
            for product in products:
                try:
                    name = product.find_element(By.XPATH, '//h2[contains(@class, "3gj")]').text
                    price_text = product.find_element(By.XPATH, '//span[contains(@class, "uiPriceSimpleScss")]').text
                    price = str(price_text.replace(' ', '').replace(',', '.'))
                    smartphones.append({'name': name, 'price': price, 'source': 'Neonet'})
                except Exception as e:
                    print(f'Error extracting data: {e}')

            next_button = driver.find_element(By.XPATH, '//*[@id="mainColumn"]/section[2]/button')
            if next_button:
                next_button.click()
                time.sleep(5)  # Czekaj, aby następna strona się załadowała
            else:
                break
        except Exception as e:
            print(f'Error: {e}')
            break

    return smartphones
def get_smartphones_xkom(min_price):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get('https://www.x-kom.pl/')
    time.sleep(5)
    accept = driver.find_element(By.XPATH, '//*[@id="react-portals"]/div[11]/div/div/div/div[3]/button[2]')
    accept.click()
    search = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/header/div[2]/div/div[2]/div[1]/div/div/div/div[1]/input')
    search.send_keys('smartfon')
    search.send_keys(Keys.ENTER)
    time.sleep(3)
    set_price = driver.find_element(By.XPATH,'//*[@id="listing-filters"]/div[2]/div/section[2]/div/div/div/div[1]/div/input')
    set_price.send_keys('3000')
    set_price.send_keys(Keys.ENTER)
    time.sleep(10)

    smartphones = []
    page_number = 1
    while True:
        try:
            products = driver.find_elements(By.XPATH, '//h3[contains(@class, "dqjhiw")]')
            for product in products:
                try:
                    name = product.find_element(By.XPATH, '//h3[contains(@class, "dqjhiw")]').text
                    price_text = product.find_element(By.XPATH, '//span[contains(@class, "dTaXAZ")]').text
                    price = str(price_text.replace(' ', '').replace(',', '.'))
                    smartphones.append({'name': name, 'price': price, 'source': 'X-Kom'})
                except Exception as e:
                    print(f'Error extracting data: {e}')

            if page_number == 1:
                # XPath dla pierwszej strony
                next_button_xpath = '//*[@id="listing-container-wrapper"]/div[4]/div[2]/a'
            else:
                # XPath dla pozostałych stron
                next_button_xpath = '//*[@id="listing-container-wrapper"]/div[4]/div[2]/a[2]'

            try:
                next_button = driver.find_element(By.XPATH, next_button_xpath)
                next_button.click()
                page_number += 1
                time.sleep(5)
            except Exception as e:
                print(f'Brak kolejnej strony: {e}')
                break

        except Exception as e:
            print(f'Error: {e}')
            break

    return smartphones

min_price = 3000
smartphones_neonet = get_smartphones_neonet(min_price)
smartphones_xkom = get_smartphones_xkom(min_price)

print("Liczba pobranych produktów:", len(smartphones_neonet))
print("Przykładowy produkt:", smartphones_neonet[0] if smartphones_neonet else None)
print("Liczba pobranych produktów:", len(smartphones_xkom))
print("Przykładowy produkt:", smartphones_xkom[0] if smartphones_xkom else None)

df = pd.DataFrame(smartphones_neonet)
df.to_csv('smartphones_neonet.csv', index=False)
df = pd.DataFrame(smartphones_xkom)
df.to_csv('smartphones_xkom.csv', index=False)
print('Dane zostały zapisane do pliku')

comparison = df.groupby(['name', 'source']).agg({'price': 'min'}).unstack()
print(comparison)



