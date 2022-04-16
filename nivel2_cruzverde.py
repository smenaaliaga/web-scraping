from scrapy.item import Field, Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor

class Producto(Item) :
    Nombre = Field()
    Producto = Field()

class CruzVerde(CrawlSpider) :
    name = 'CruzVerdeSpider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ["https://www.cruzverde.cl/medicamentos/"]
    allowed_domains = ['cruzverde.cl']
    download_delay = 1
    rules = (
        Rule(
            LinkExtractor(
                allow = r'start=',
                # Busca en los tags 'a' y 'button'
                tag = ('a', 'button'),
                # en los atributos 'href' y 'data-url'
                attrs = ('href', 'data-url')
            ), follow = True, callback = 'parse_cruzverde'
        )
    )
    def parse_cruzverde(self, response) :
        sel = Selector(response)
        productos = sel.xpath('//ml-card-product')
        for producto in productos :
            item = ItemLoader(Producto(), producto)
            item.add_xpath('Nombre', '//ml-card-product//at-link//span/text()')
            item.add_xpath('Precio', '//ml-price-tag//span/text()')

            yield item.load_item()