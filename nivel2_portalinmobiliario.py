from scrapy.item import Field, Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor

class Depto(Item) :
    nombre = Field()
    precio = Field()
    gasto_comun = Field()
    
class HotelSpider(CrawlSpider) :
    # Nombre del Spider
    name = "HotelSpider"
    # Configuración del USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ["https://www.portalinmobiliario.com/arriendo/departamento/providencia-metropolitana"]
    # Tiempo que esperará Scrapy luego de cada requerimiento a cada pagina desde la URL Senilla
    RANDOMIZE_DOWNLOAD_DELAY  = True
    # Regla para extraer los datos de la URL Senilla
    rules = (
        Rule(
            LinkExtractor(
                allow = r'/MLC-'
            ), follow = True, callback = 'parse_depto'
        ),
    )
    
    #### Preprocesamiento de datos: Eliminamos el simbolo CLP del texto
    def deleteCLP(self, text) :
        newTxt = text.replace(' CLP', '')
        return newTxt
    
    def parse_depto(self, response) :
        sel = Selector(response)
        item = ItemLoader(Depto(), sel)
        
        item.add_xpath('nombre', '//h1[@class="ui-pdp-title"]/text()')
        item.add_xpath('precio', '//span[@class="andes-money-amount__fraction"]/text()')
        item.add_xpath('gasto_comun', 
                       '//div[@class="ui-pdp-specs__table"]//span[contains(text(),"CLP")]/text()',
                       MapCompose(self.deleteCLP))
        
        yield item.load_item()
        
# EJECUCION EN TERMINAL:
# scrapy runspider nivel2_portalinmobiliario.py -o results/portalinmobiliario.json -t json