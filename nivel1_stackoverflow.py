import requests
from bs4 import BeautifulSoup

head = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

url = 'https://stackoverflow.com/questions/'

res = requests.get(url, headers = head)

soup = BeautifulSoup(res.text, features="lxml")

questions = soup.find(id = "questions")

list_questions = questions.find_all('div', class_ = 's-post-summary')

for question in list_questions :
    title = question.find('a').text
    desc = question.find('div', class_ = 's-post-summary--content-excerpt').text
    desc = desc.replace('\n', '').replace('\r', '')
    print("     Titiulo: ")
    print(title)
    print(      "Descripción: ")
    print(desc)
    print("-----------------------------------------------------")