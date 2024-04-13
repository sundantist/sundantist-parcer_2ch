import pandas as pd
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions


options = ChromeOptions()
#options.add_argument("--headless=new") #Аргумент "неоткрывания" браузера
options.add_argument("--disable-webusb")
options.add_argument("user-data-dir=C:\\Users\\sundantist\\AppData\\Local\\Google\\Chrome\\User Data") # Линк на пользовательский профиль, ибо куки я в рот ебал, и не разобрался
driver = webdriver.Chrome(options=options)

driver.get("https://2ch.hk/h/")
results = []
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

def parse_image_urls(classes, location, source):
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))

#Прокрутка страницы с бесконечной загрузкой

last_height = driver.execute_script("return document.body.scrollHeight")
while True:

# Прожимаем кнопки для раскрытия тредов ??????????????????????? АЛЯРМ ВАРНИНГ ОПАСНО СУКА НЕ РАБОТАТЬ НИХУЯ
    
    button = driver.find_elements(By.CSS_SELECTOR, "/html/body/div[1]/main/div[2]/div[126]/div[2]")
    button.click()

# Парсим это говно и получаем URL пикчи

    parse_image_urls("post__image-link", "img", "data-src")

# Пролистываем "бесконечную" страницу

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(6)  # Необходимо дать время для загрузки страницы через AJAX.
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Если высота страницы не меняется, это означает, что прокрутка достигла низа.
    last_height = new_height

# Записываем эту поеботу в CSV
df = pd.DataFrame({"links": results})
df.to_csv("links.csv", index=False, encoding="utf-8")