from scrapy.item import Field, Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
import urllib3

class Auto(Item) :
    titulo = Field()
    km = Field()
    transmision = Field()
    color = Field()
    precio = Field()
    
class ChileautosCrawler(CrawlSpider) :
    # Nombre del Spider
    name = 'ChileautosCrawler'
    # Configuración del USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # Cantidad pagina maxima a descargar
        'CLOSESPIDER_PAGECOUNT' : 5
    }
    # Regla para solo ingresar a los dominios de Chileautos
    allowed_domains = ['chileautos.cl']
    # URL Semilla
    start_urls = ["https://www.chileautos.cl/vehiculos/autos-vehículo/audi/"]
    # Random delay para ingresas a las paginas
    RANDOMIZE_DOWNLOAD_DELAY  = True
    
    FEED_EXPORT_ENCODING = 'utf-8'
    # Reglas
    rules = (
        # REGLA #1 => HORIZONTALIDAD POR PAGINACION
        Rule(
            LinkExtractor(
                allow = r'/?offset=\d+'
            ), follow = True
        ),
        # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
        Rule(
            LinkExtractor(
                allow = r'/vehiculos/detalles/'
            ), follow = True, callback = 'parse_autos'
        ),
    )
    
    def to_write(uni_str):
        return urllib3.unquote(uni_str.encode('utf8')).decode('utf8')


    def parse_autos(self, response) :
        sel = Selector(response)
        item = ItemLoader(Auto(), sel)
        item.add_xpath('titulo', '//div[@class="details-title full-width"]//h1/text()') 
        item.add_xpath('km', 
                       '//div[@class="col features-item-value features-item-value-kilmetros"]/text()', 
                       MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip())
                       )
        item.add_xpath('transmision', '//div[@class="key-details-item" and position()=2]//div[@class="key-details-item-title"]/text()')
        item.add_xpath('color', 
                       '//div[@class="col features-item-value features-item-value-color"]/text()',
                       MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip())
                       )
        item.add_xpath('precio', '//div[@class="col default-price text-left"]/data-default-price-value')
        
        yield item.load_item()
        
# EJECUCION EN TERMINAL:
# scrapy runspider nivel2_chileautos.py -o results/chileautos.json -t json