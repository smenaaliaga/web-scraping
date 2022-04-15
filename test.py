from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor

class Depto(Item) :
    nombre = Field()
    precio = Field()
    gasto_comun = Field()

class PortainmobiliarioSpider(CrawlSpider) :
    # Nombre del Spider
    name = "PortainmobiliarioSpider"
    # Configuración del USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ["https://www.portalinmobiliario.com/arriendo/departamento/metropolitana"]
    allowed_domains = ['portalinmobiliario.com']
    # Tiempo que esperará Scrapy luego de cada requerimiento a cada pagina desde la URL Senilla
    RANDOMIZE_DOWNLOAD_DELAY  = True
    # Regla para extraer los datos de la URL Senilla
    rules = (
        Rule(
            LinkExtractor(
                allow = r'/departamento/',
                restrict_xpaths = r'//div[./div[@class="ui-search-filter-dt-title" and contains(text(),"Ciudades")]]'
            ), follow = True #, callback = 'parse_false'
        ),
    )

    def parse_false(self, response) :
        sel = Selector(response)
        item = ItemLoader(Depto(), sel)

        yield item.load_item()

        
# EJECUCION EN TERMINAL:
# scrapy runspider test.py -o results/test.json -t json
