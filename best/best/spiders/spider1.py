import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher


class Spider1(scrapy.Spider):
    name = 'bo'
    allowed_domains = ['bestbuy.com']
    start_urls = ['https://www.bestbuy.com/site/searchpage.jsp?st=acces+point&intl=nosplash']

    custom_settings = {
        'FEED_FORMAT': "csv",
        'FEED_URI': "products.json"
    }
    words = ["access poit"]  # here is the list of words u want to use

    '''
    this function will generate the url of each word 
    '''
    def start_requests(self):
        for word in self.words:
            link = f"https://www.bestbuy.com/site/searchpage.jsp?st={word.replace(' ', '+')}&intl=nosplash"
            print(link)
            yield scrapy.Request(link, callback=self.parse, meta={'page':0})


    def parse(self, response):

        product_links = response.xpath('//h4/a/@href').getall()
        for link in product_links:
            k = f'https://www.bestbuy.com/{link}'
            yield scrapy.Request(k, callback=self.parse_products)

        next = response.xpath('//a[@class="sku-list-page-next"]/@href').get()

        if next is not None and response.meta['page'] < 3:
            r = f'https://www.bestbuy.com/{next}'
            print(f"next url {r}")
            yield scrapy.Request(r, callback=self.parse , meta={'page':response.meta['page']+1})

    '''
    here You can modify the code simply by changing the xpathes of each property 
    and add them in the yield block down as shown. for ex, if u want to add prodcut specification ,
    You can define it like this:
    product_specification = response.xpath('//according xpath').get()
    then
    add it in the yield block
    "Product specification":product specification, 
    '''
    def parse_products(self, response):
        product_url = response.url
        product_name = response.xpath('//h1[@class="heading-5 v-fw-regular"]/text()').get()
        price = response.xpath('//div[@class="pricing-price"]/div/div/div/div/div/div/div/div/span/text()').get()
        rate = response.xpath('//span[@class="popover-wrapper"]/a/div/p/text()').get()
        img = response.xpath('//button[@class="primary-button"]/img/@src').get()
        SKU = response.xpath(
            '//div[@class="sku product-data"]/span[@class="product-data-value body-copy"]/text()').get()
        Model = response.xpath(
            '//div[@class="model product-data"]/span[@class="product-data-value body-copy"]/text()').get()
        yield {

            "HTML": response.body,
        }


'''
this function will return u a list with all products and each item in a list will be a dictionary like this:
{"Product name":name, "Price":price, "Rate":rate,"Image": img,"Product URL": product_url,"SKU":SKU,"Model":Model,"HTML":response.body,}

if u don't need any element of these u can delete it from the yield block in the above function 
'''

def spider_results():
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(Spider1)
    process.start()  # the script will block here until the crawling is finished    return results


if __name__ == "__main__":

    x = spider_results() # this list will hold the whole products
    print("This is the first element in the list")
    print(x[0])
