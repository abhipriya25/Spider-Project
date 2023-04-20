# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
# from locations import categories
from locations.operations import extract_phone, extract_email

# class CategoryPipeline(object):

#     def get_category(self, category_code):
#         return categories.full_list[category_code]['category']

#     def process_item(self, item, spider):
#         if hasattr(spider, 'categories'):
#             item['categories'] = [self.get_category(category_code) for category_code in spider.categories]
            
#         return item


class NormalizationPipeline(object):
    def process_item(self, item, spider):
        
        if 'phone' in item and item.get('phone') != None:
            phones = item.get('phone')
            item['phone'] = [extract_phone(phone) for phone in phones if phone != None]
        else:
            item['phone'] = []

        if 'email' in item and item.get('email') != None:
            emails = item.get('email')
            item['email'] = [extract_email(email) for email in emails if email != None]
        else:
            item['email'] = []
        
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        ref = (spider.name, item['ref'])
        if ref in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(ref)
            return item


class ApplySpiderNamePipeline(object):

    def process_item(self, item, spider):
        existing_extras = item.get('extras', {})
        existing_extras['@spider'] = spider.name
        # existing_extras['@mode'] = spider.mode
        # existing_extras['@categories'] = spider.categories
        item['extras'] = existing_extras

        return item

class ApplySpiderLevelAttributesPipeline(object):
    def process_item(self, item, spider):
        if not hasattr(spider, 'item_attributes'):
            return item

        item_attributes = spider.item_attributes
        
        for (key, value) in item_attributes.items():
            if key not in item:
                item[key] = value

        return item