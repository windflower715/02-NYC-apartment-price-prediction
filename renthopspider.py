import scrapy


class renthop(scrapy.Spider):
    name = 'manhattan_listing'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://www.renthop.com/nyc/manhattan-apartments']

    def parse(self, response):
        listing_links = response.xpath('//div[@class="media-body overflow-ellipsis"]/div//@href').extract()
        for i in range(len(listing_links)):
            yield scrapy.Request(
                url=listing_links[i],
                callback=self.parse_unit,
                meta={'url':listing_links})

        next_url = 'http://www.renthop.com'+response.xpath('//a[contains(., "Next")]/@href').extract_first()
        # returns partial url for next page
        yield scrapy.Request(
            url=next_url,
            callback=self.parse
            )
    def parse_unit(self,response):
        beds = response.xpath('//td[contains(., "Bed")]/text()').extract_first()
        bath = response.xpath('//td[contains(.,"Bath")]/text()').extract_first()
        sqft = response.xpath('//td[contains(., "Sqft")]/text()').extract_first()
        train = response.xpath('//span[@style="color: black; font-weight: bold"]/text()').extract_first()
        features = response.xpath('//div[@class="columns-2"]/div/text()').extract()
        address = response.xpath('//h1[@class="d-none d-lg-block overflow-ellipsis vitals-title"]/text()').extract_first()
        monthlyrent = response.xpath('//div[@class="font-light-green b vitals-title text-left text-lg-right"]/text()').extract_first().strip()
        hopscore = float(response.xpath('//div[@class="font-blue b vitals-title"]/text()').extract_first().strip())
        neighborhood = response.xpath('//div[@class="overflow-ellipsis font-size-10"]/text()').extract_first().split(',')[1].strip()

        #monthlyrent = response.xpath('//div[@class="font-light-green b vitals-title text-left text-lg-right"]/text()').extract_first().strip()
        #train = response.xpath('//span[@style="color: black; font-weight: bold"]/text()').extract_first()
        #features = response.xpath('//div[@class="columns-2"]/div/text()').extract()
        #address = response.xpath('//h1[@class="d-none d-lg-block overflow-ellipsis vitals-title"]/text()').extract_first()



        

        yield {'beds':beds, 'bath':bath,'sqft':sqft,'train':train,'features':features,'address':address,'monthlyrent':monthlyrent,'hopscore':hopscore,'neighborhood':neighborhood}

        # Follow pagination links and repeat