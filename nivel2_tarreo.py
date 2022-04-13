from scrapy.item import Field, Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor

class Juego(Item) :
    titulo = Field()
    genero = Field()
    
class Articulo(Item) :
    encabezado = Field()
    escritor = Field()
    
class Review(Item) :
    titulo = Field()
    rating = Field()
    
class TarreoCrawler(CrawlSpider) :
    name = "TarreoCrawler"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ["https://www.tarreo.com/juegos", "https://www.tarreo.com/articulos", "https://www.tarreo.com/reviews"]
    allowed_domain = ['tarreo.com']
    RANDOMIZE_DOWNLOAD_DELAY  = True
    rules = (
        # Regla por cada tipo de información
        # Juegos
        Rule(
            LinkExtractor(
                allow = r'/PC/juegos/'
            ), follow = True, callback = 'parse_juego' 
        ),
        # Articulos
        Rule(
            LinkExtractor(
                allow = r'/articulos/'
            ), follow = True, callback = 'parse_articulo'
        ),
        # Reviews
        Rule(
            LinkExtractor(
                allow = r'/review'
            ), follow = True, callback = 'parse_review'
        ), 
    )
    
    def parse_juego(self, response) :
        item = ItemLoader(Juego(), response)
        
        item.add_xpath('titulo', '//h1/span/text()')
        item.add_xpath('genero', '//meta[@itemprop="genre"]/@content')
        
        yield item.load_item()

    def parse_articulo(self, response) :
        item = ItemLoader(Articulo(), response)
        
        item.add_xpath('encabezado', '//div[@class="header_background"]//h1/text()')
        item.add_xpath('escritor', '//div[@class="post-infoContainer cf"]//a/span/text()')
        
        yield item.load_item()
        

    def parse_review(self, response) :
        item = ItemLoader(Review(), response)
        
        item.add_xpath('titulo', '//div[@class="review_info"]//h1/text()')
        item.add_xpath('rating', '//canvas[@class="rating_container rating"]/@rating')
        
        yield item.load_item()
        
# EJECUCION EN TERMINAL:
# scrapy runspider nivel2_tarreo.py -o results/tarreo.json -t json