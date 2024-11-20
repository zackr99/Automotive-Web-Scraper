import requests
from bs4 import BeautifulSoup
import io
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from PyPDF2 import PdfFileReader

class Crawler(CrawlSpider):

    def __init__(self, search_term=None, *args, **kwargs):
        super(Crawler, self).__init__(*args, **kwargs)
        self.search_term = search_term

    name = 'manuals'
    allowed_domains = ['www.auto-brochures.com']
    start_urls = ['https://www.auto-brochures.com/']
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 10000,
        'CONCURRENT_REQUESTS': 20,  # Increase to a higher value
            'ITEM_PIPELINES': {'web_crawler.pipelines.CustomFilesPipeline': 1},
        'FILES_STORE': '/Users/zackchand/Downloads/pdfs',  # Path where the files are stored 
    }
    rules = (
        Rule(
        LinkExtractor(allow=('\.pdf$',)),
        callback='parse_pdf',
        follow=True,
        ),
        Rule(
        LinkExtractor('\.html$',),  # Default: Extract all links
        callback='parse_html',
        follow=True,
        ),
    )

    def parse_pdf(self, response):
    # Check if the URL ends with .pdf and the response is a PDF by checking the content-type header
    
        if response.url.lower().endswith('.pdf'):
          
          yield {
              'file_urls': [response.url],
              'name': self.search_term
           }
    def parse_html(self, response):
        # Process HTML pages here
        # Example: Extract data, scrape additional links, etc.
         if(response.url.lower().endswith('.html')):
            #TEST see if the search term is correctly being appended
            print(self.search_term)
            if self.search_term in response.url:
            #TEST see if html is found
            #print("HTML IS FOUND")
            #TEST extract the links from the html page
                links = response.css('a::attr(href)').extract()
                #print("LINKS: " , links)
                #Currently the links are going to the html pages
                #We need to enter the pages
                for link in links:
                    #Check to see if page is html
                    if link.endswith('.html'):
                        #Enter the link and recursively call until PDF is found
                        yield scrapy.Request(url=response.urljoin(link), callback=self.parse_html)
                    #Otherwise if the link ends with a pdf
                    elif link.lower().endswith('.pdf'):
                        #Download the PDF file
                        yield scrapy.Request(url=response.urljoin(link), callback=self.parse_pdf)



        # You can add your logic to process HTML pages here if needed
