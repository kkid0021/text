import scrapy

class WeatherItem(scrapy.Item):
    city = scrapy.Field()
    date = scrapy.Field()
    temperature = scrapy.Field()
    humidity = scrapy.Field()
    wind_strength = scrapy.Field()

class WeatherSpider(scrapy.Spider):
    name = 'weather'
    start_urls = ['https://www.tianqi.com/nanjing/']

    def parse(self, response):
        item = WeatherItem()
        item['city'] = response.xpath('//h1/text()').get()
        item['date'] = response.xpath('//dd[@class="week"]/text()').get()
        item['temperature'] = response.xpath('//p[@class="now"]/b/text()').get()
        item['humidity'] = response.xpath('//dd[@class="shidu"]/b[1]/text()').get()
        item['wind_strength'] = response.xpath('//dd[@class="shidu"]/b[2]/text()').get()
        yield item

        
class WeatherPipeline(object):
    def open_spider(self, spider):
        self.file = open('weather.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write('city: ' + item['city'] + '\n')
        self.file.write('date: ' + item['date'] + '\n')
        self.file.write('temperature: ' + item['temperature'] + '℃\n')
        self.file.write('humidity: ' + item['humidity'] + '\n')
        self.file.write('wind_strength: ' + item['wind_strength'] + '\n')
        return item
