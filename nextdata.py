import httpx
import bs4
import json

url = "" #put url here
a = httpx.get(url).text
soup = bs4.BeautifulSoup(a, features = "lxml")
b = soup.find_all('script')
for item in b:
    if not item.get("src") and not item.get("type"): #next data is the only script tag without any src or type attributes
        c = item

data = c.contents[0].split("\n")[1][26:]