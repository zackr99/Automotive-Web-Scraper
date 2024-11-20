# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request

class CustomFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        # This method is called for every item pipeline component
        for file_url in item['file_urls']:
            yield Request(file_url, meta={'name': item['name']})
            
    def file_path(self, request, response=None, info=None):
        # Extract the filename from the URL and append the search term
        # Assuming the search term is passed in the item and is safe to use as a filename
        original_file_name = request.url.split('/')[-1]
        search_term = request.meta['name']  # Use the search term from the item's metadata
        # Create a new filename. You might want to include additional logic here to ensure uniqueness
        new_file_name = f"{search_term}_{original_file_name}"
        return new_file_name
