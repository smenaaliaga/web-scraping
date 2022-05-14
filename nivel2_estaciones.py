from scrapy.item import Field, Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

class Estacion(Item) :
    linea = Field()
    nombre = Field()
    lat = Field()
    long = Field()
    
class LatLongEstaciones(CrawlSpider) :
    name = "LatLongEstaciones"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = [
        'https://es.wikipedia.org/wiki/Línea_1_del_Metro_de_Santiago', 
        'https://es.wikipedia.org/wiki/Línea_2_del_Metro_de_Santiago', 
        'https://es.wikipedia.org/wiki/Línea_3_del_Metro_de_Santiago',
        'https://es.wikipedia.org/wiki/Línea_4_del_Metro_de_Santiago',
        'https://es.wikipedia.org/wiki/Línea_4A_del_Metro_de_Santiago',
        'https://es.wikipedia.org/wiki/Línea_5_del_Metro_de_Santiago',
        'https://es.wikipedia.org/wiki/Línea_6_del_Metro_de_Santiago'
        ]
    RANDOMIZE_DOWNLOAD_DELAY  = True
    rules = (
        Rule(
            LinkExtractor(
                allow = r'/wsiki/',
                attrs = ('href'),
                restrict_xpaths = (
                    '//div[@class="mw-parser-output"]//tr/td[@style="text-align:center;"]/table')
            ), callback = 'parse_nombre_estaciones' 
        ),
        Rule(
            LinkExtractor(
                allow = r'/geohack.php',
                deny_domains = r'wikipedia.org'
            ), callback = 'parse_latlong_estaciones' 
        ),
    )

    def parse_nombre_estaciones(self, response) :
        item = ItemLoader(Estacion(), response)
        
        item.add_xpath('nombre', '//tr/th[@class="cabecera"]/text()')

        yield item.load_item()
    
    def parse_latlong_estaciones(self, response) :
        item = ItemLoader(Estacion(), response)
        
        item.add_xpath('lat', '//span[@class="latitude"]/text()')
        item.add_xpath('long', '//span[@class="longitude"]/text()')

        yield item.load_item()

# Deploy
path = 'results/'
process = CrawlerProcess(settings={
    "FEEDS": {
        path + 'estaciones.csv' : {"format": "csv"},
    },
})
process.crawl(LatLongEstaciones)
process.start()
# EJECUCION EN TERMINAL:
# scrapy runspider nivel2_estaciones.py -o results/estaciones.csv -t csv