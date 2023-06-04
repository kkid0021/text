import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

#Items类
class WeatherItem(scrapy.Item):
    date = scrapy.Field()
    temperature = scrapy.Field()
    humidity = scrapy.Field()
    city = scrapy.Field()

#spider类
class WeatherSpider(scrapy.Spider):
    name = 'weather_spider'
    start_urls = ['https://www.tianqi.com/nanjing/'] # 想要爬取的城市的天气预报网页

    def parse(self, response):
        yield {
            'city': response.xpath('//h1/text()').get(),
            'date': response.xpath('//dd[@class="week"]/text()').get(),
            'temperature': response.xpath('//p[@class="now"]/b/text()').get(),
            'humidity': response.xpath('//dd[@class="shidu"]/b[1]/text()').get(),
            
        }
#Pipeline类
class WeatherPipeline(object):
    def open_spider(self, spider):
        self.file = open('weather.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = f"{item['city']}{item['date']} {item['temperature']} {item['humidity']} \n"
        self.file.write(line)
        return item

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'ITEM_PIPELINES': {'__main__.WeatherPipeline': 300}
    })
    process.crawl(WeatherSpider)
    process.start()
