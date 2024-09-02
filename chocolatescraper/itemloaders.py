from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

class ChocolateProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    price_in = MapCompose(str.strip, lambda x: float(x.replace('£', '')))
    url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x)