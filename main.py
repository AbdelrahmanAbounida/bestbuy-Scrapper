from bs4 import BeautifulSoup
import requests


with requests.Session() as s:
    url = 'https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/scholarship-amount/varies/make-a-ripple-change-the-world-kindness-action-competition'
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    a = soup
    print(a)
    print(r.url)
