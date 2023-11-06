from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import re

class Hotel(Item):
    nombre = Field()
    direccion = Field()
    telefono= Field()
    rango_precios = Field()
    habitaciones = Field()
    opiniones = Field()
    facilidades = Field()
    calificacion = Field()
    ubicacion = Field()    
    limpieza = Field()
    servicio = Field()
    calidad_precio=Field()

class TripAdvisor(CrawlSpider):
    name = "Test"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'FEED_EXPORT_FIELDS': ["nombre","calificacion","ubicacion","limpieza","servicio","calidad_precio","rango_precios","habitaciones","opiniones","direccion","telefono","facilidades"],
        'CLOSESPIDER_PAGECOUNT': 100
    }     

    start_urls = ['https://www.tripadvisor.com.mx/Hotels-g150782-Monterrey_Northern_Mexico-Hotels.html']
    
    dowload_delay = 2

    rules = (
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-'
            ),follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r"/Hotel_Review-",
                restrict_xpaths=["//div[@data-automation='hotel-card-title']"] 
            ),follow=True,callback="Hotel"
        ),
    )
    def limpiar(self,cadena):
        if cadena.startswith("$") == True:
            return cadena.replace("$","").replace(",","")
    
    def expresion(self,cadena):
        if re.search(r'\d',cadena):
            return cadena.replace(",","")

    def Hotel(self,response):
        sel = Selector(response)
        item= ItemLoader(Hotel(),sel)

        item.add_xpath("nombre","//h1[@id='HEADING']/text()")
        item.add_xpath("opiniones", "//span[@class='hkxYU q Wi z Wc']/text()",MapCompose(self.expresion))
        item.add_xpath("direccion","(//span[@class='fHvkI PTrfg'])[1]/text()")
        item.add_xpath("telefono","(//span[@class='zNXea NXOxh NjUDn'])[1]/text()")
        item.add_xpath("facilidades","//div[@data-test-target='amenity_text']/text()")
        item.add_xpath("rango_precios","(//div[@class='IhqAp Ci'])[1]/text()",MapCompose(self.limpiar))
        item.add_xpath("habitaciones","(//div[@class='IhqAp Ci'])[last()]/text()")
        item.add_xpath("calificacion","(//div[@id='ABOUT_TAB']//span[contains(@class,'ui_bubble_rating bubble_')])[1]/@class",MapCompose(lambda x: x.split(" ")[1].split("_")[1]))
        item.add_xpath("ubicacion","(//div[@id='ABOUT_TAB']//span[contains(@class,'ui_bubble_rating bubble_')])[2]/@class",MapCompose(lambda x: x.split(" ")[1].split("_")[1]))
        item.add_xpath("limpieza","(//div[@id='ABOUT_TAB']//span[contains(@class,'ui_bubble_rating bubble_')])[3]/@class",MapCompose(lambda x: x.split(" ")[1].split("_")[1]))
        item.add_xpath("servicio","(//div[@id='ABOUT_TAB']//span[contains(@class,'ui_bubble_rating bubble_')])[4]/@class",MapCompose(lambda x: x.split(" ")[1].split("_")[1]))
        item.add_xpath("calidad_precio","(//div[@id='ABOUT_TAB']//span[contains(@class,'ui_bubble_rating bubble_')])[5]/@class",MapCompose(lambda x: x.split(" ")[1].split("_")[1]))
        yield item.load_item()


