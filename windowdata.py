import httpx
import bs4 
import json

url = "" #put url here
a = httpx.get(url).text
soup = bs4.BeautifulSoup(a, features="lxml")
b = soup.find_all('script')
longest = 0 #window.__data is the longest script tag, so we can extract it that way
out = ""
for item in b:
    if item.get("charset") and item.get("nonce"): #window.__data always has these attributes
        if len(str(item)) > longest:
            longest = len(str(item))
            out = item

data = json.loads(out.contents[0][14:-1]) #json data ready to use 