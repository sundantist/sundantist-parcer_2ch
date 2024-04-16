import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

url = 'https://2ch.hk/h/'
thread_list = []
thread_list_sort = []

options = ChromeOptions()
#options.add_argument("--headless=new") #Аргумент "неоткрывания" браузера, на время отладки пусть лежит в коментах
options.add_argument("--disable-webusb")
options.add_argument("user-data-dir=C:\\Users\\sundantist\\AppData\\Local\\Google\\Chrome\\User Data") # Линк на пользовательский профиль, ибо куки я в рот ебал, и не разобрался
driver = webdriver.Chrome(options=options)

driver.get(url)
content = driver.page_source
soup = BeautifulSoup(content, 'lxml')
all_thread_link = soup.find_all(attrs={"class" : "post__reflink"})



# Запись html страницы в файл для удобства отладки
html_file = open("html.index", "w+", encoding="utf-8")
html_file.write(str(soup))
html_file.close()

# Декоратор

#def scroll_decorator(func):
    #def wrapper():
        #last_height = driver.execute_script("return document.body.scrollHeight")
        #while True:
            #func()
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #time.sleep(4)  # Необходимо дать время для загрузки страницы через AJAX.
            #new_height = driver.execute_script("return document.body.scrollHeight")
            #if new_height == last_height:
                #break  # Если высота страницы не меняется, это означает, что прокрутка достигла низа.
            #last_height = new_height
    #return wrapper

# Функция для получения списка с номерами тредов

def get_number_of_thread():
# Получение линков на треды, но тут еще прочее говно
    thread_list = []
    thread_list_sort = []
    for item in all_thread_link:
        item_link = item.get("href")
        print(item_link) #################################################################
        if item_link not in thread_list:
            symbols_to_remove = "." # Убираем точки из строки
            for symbol in symbols_to_remove:
                item_link = item_link.replace(symbol, '')
            thread_list.append('2ch.hk' + item_link[0:13]) # Делаем срез для удобства будущей сортировки 
# Уничтожение повторяющихся позиций в списке
    for num in thread_list:
        if num not in thread_list_sort:
            thread_list_sort.append(num)
    return thread_list_sort

# Прокрутка страницы
def scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Необходимо дать время для загрузки страницы через AJAX.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Если высота страницы не меняется, это означает, что прокрутка достигла низа.
        last_height = new_height

#--------------------------------------------------------------------------------------------------------- Отладка
scroll()
print(get_number_of_thread())
