import scrapy
import os
import csv

class OlSpider(scrapy.Spider):
    name = 'ol'
    start_urls = ['https://olhardigital.com.br/author/isabela-gusmao/']

    if os.path.exists("result.csv"):
        os.remove("result.csv")

    def parse(self, response, **kwargs):
        for i in response.xpath('//a[@class="card-post type8 img-effect1"]'):
            link = i.xpath('./@href').get()
            yield scrapy.Request(link,callback=self.parse_text)
    
    def parse_text(self, response):
        title = response.xpath('//div[@class="container"]//h1/text()').get()
        if not title:
            title = response.xpath('//div[@class="banner banner-video"]//h1/text()').get()
        content = ""
        for line in response.xpath('//div[@class="post-content wp-embed-responsive"]//p/text()').getall():
            content = content + "".join(line.strip()) + " "
        result = {
            "title": title,
            "content": content,
            "author": "Isabela Valukas Gusmão"
        }
        with open('result.csv', 'a', newline='', encoding="utf-8") as output_file:
             dict_writer = csv.DictWriter(output_file, result.keys(),delimiter='|')            
             dict_writer.writerows([result])
        return result
        
