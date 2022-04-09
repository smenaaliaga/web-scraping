import requests
from lxml import html

# Header le dice al servidor que navegador y sistema operativo estoy utilizado 
# Si no se lo digo, el servidor lo toma como un bot
head = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

url = 'https://www.wikipedia.org/'

# Obtener respuesta GET
res = requests.get(url, headers = head)

# Parsea la respuesta a HTML
parser = html.fromstring(res.text)

# Obtener el texto ingles del id especifico
ingles = parser.xpath("//a[@id='js-link-box-en']/strong/text()")

# Obtener los idiomas disponibles de wikipedia
idiomas = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong    /text()")

for idioma in idiomas:
    print(idioma)
