import requests 
from bs4 import BeautifulSoup 
	
def getdata(url): 
	r = requests.get(url) 
	return r.text 
	
htmldata = getdata("https://2ch.hk/b/") 
soup = BeautifulSoup(htmldata, 'html.parser') 
for item in soup.find_all('href'): 
	print(item['src'])
