import pandas as pd
import time
#import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains


options = ChromeOptions()
#options.add_argument("--headless=new") #Аргумент "неоткрывания" браузера, на время отладки пусть лежит в коментах
options.add_argument("--disable-webusb")
options.add_argument("user-data-dir=C:\\Users\\sundantist\\AppData\\Local\\Google\\Chrome\\User Data") # Линк на пользовательский профиль, ибо куки я в рот ебал, и не разобрался
driver = webdriver.Chrome(options=options)

driver.get("https://2ch.hk/h/")
results = []
tread_list = []
tread = []
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")


# Метод парсинга картинок без запросов

def parse_image_urls(classes, location, source):
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append("2ch.hk" + name.get(source))

# Метод проверки "нового" треда
def check_tread(number_of_tread):
    if number_of_tread in tread_list:
        return(True)
    else:
        tread_list.append(number_of_tread)
        return(False)

# Метод для парсинга номера треда

def parse_number_of_tread(classes, location, source):
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in tread:
            tread.append(name.get(source)) # Не очень понятно нахуя мне нужны эти две строчки, пока пусть будут
            print("\n", name)
            print("\n", name.get(source))
        return(name.get(source))

#def parse_number_of_tread():
#    xpath = ""
#    element = driver.find_element(By.XPATH, xpath)
#    print("АБОБА", element)

#Прокрутка страницы с бесконечной загрузкой

last_height = driver.execute_script("return document.body.scrollHeight")
while True:

# Парсим это говно и получаем URL пикчи

    if check_tread(parse_number_of_tread("thread", "div", "data-num")):
        print(parse_number_of_tread("thread", "div", "data-num"))
        parse_image_urls("post__image-link", "img", "data-src")
        print("Все заебись, ебошим")
    else:
        print("Чет не так :(")
    


# Пролистываем "бесконечную" страницу

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Необходимо дать время для загрузки страницы через AJAX.
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Если высота страницы не меняется, это означает, что прокрутка достигла низа.
    last_height = new_height

# Отладочное говно

print("\n\n\n\n",tread_list)

# Записываем эту поеботу в CSV

df = pd.DataFrame({"links": results})
df.to_csv("./csv/links.csv", index=False, encoding="utf-8")