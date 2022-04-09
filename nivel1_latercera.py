from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

# Clase Noticia para encapsular los datos que voy a extraer en La Tercera
class Noticia(Item) :
    descripcion = Field()
    tag = Field()
    titular = Field()
    
class ElUniversoSpider(Spider) :
    # Nombre del spider
    name = "LaTerceraSipider"
    # Configuración del USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    # URL SEMILLA
    start_urls = ['https://www.latercera.com/lo-ultimo/']
    
    # Función que se llama para realziar el requerimiento de la URL semilla
    def parse(__self__, response) :
        # Selector que extrae los datos de la URL semilla
        sel = Selector(response) 
        # Selector de noticias de la seccióm Ultimas Noticias de La Tercera
        noticias = sel.xpath('//div[@class="archive-list | subgrid"]//article')
        # Recorrer cada noticia
        for noticia in noticias :
            # Instancia del Item con el selector para llenar los datos de la clase Noticia
            item = ItemLoader(Noticia(), noticia)
            # Escritura de las propiedades de la clase Noticia
            item.add_xpath('descripcion', './/p/text()')
            item.add_xpath('tag', './/a/span/text()')
            item.add_xpath('titular', './/h3/a/text()')
            
            # Escritura de los resultados en el archivo de salida
            yield item.load_item()
            
# EJECUCION EN TERMINAL:
# scrapy runspider nivel1_latercera.py -o latercera.csv -t csv