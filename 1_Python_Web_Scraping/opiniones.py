from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Opinion(Item):
    autor = Field()
    titulo = Field()
    comentario = Field()
    calificacion = Field()
    fecha = Field()
    hotel = Field()

class Opiniones_Hotel(CrawlSpider):
    name = "Test"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'FEED_EXPORT_FIELDS': ["calificacion","fecha","hotel","autor","titulo","comentario"],
        'CLOSESPIDER_PAGECOUNT': 6000
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
            ),follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'-or\d+-',
            ),follow=True,callback= "Opiniones"
        ),
        )

    def fecha(self,fecha):
        fecha_nueva= " ".join(fecha.replace("de","").split())
        month,year= fecha_nueva.split(" ")
        months = {
            "enero":"01",
            "febrero":"02",
            "marzo":"03",
            "abril":"04",
            "mayo":"05",
            "junio":"06",
            "julio":"07",
            "agosto":"08",
            "septiembre":"09",
            "octubre":"10",
            "noviembre":"11",
            "diciembre":"12"
            }
        return f"{year}-{months[(month)]}-01"
    
    def Opiniones(self,response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@data-test-target="reviews-tab"]//div[@data-test-target="HR_CC_CARD"]')
        hotel = sel.xpath("//h1[@id='HEADING']/text()").get()
        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_value("hotel", hotel)
            item.add_xpath('titulo', './/div[@data-test-target="review-title"]//span/span/text()')
            item.add_xpath("fecha",".//span[@class='teHYY _R Me S4 H3']/text()",MapCompose(self.fecha))
            item.add_xpath("autor",'.//a[@class="ui_header_link uyyBf"]/text()')
            item.add_xpath('comentario', './/span[@class="QewHA H4 _a"]/span/text()')
            item.add_xpath('calificacion', './/div[@data-test-target="review-rating"]/span/@class',MapCompose(lambda x: x.split("_")[-1]))
            yield item.load_item()