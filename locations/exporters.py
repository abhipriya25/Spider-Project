# -*- coding: utf-8 -*-

import base64
import hashlib
import logging
from scrapy.exporters import JsonLinesItemExporter, JsonItemExporter
from scrapy.utils.python import to_bytes
from locations import categories

mapping = (
    ('addr_full', 'addr:full'),
    ('housenumber', 'addr:housenumber'),
    ('street', 'addr:street'),
    ('city', 'addr:city'),
    ('state', 'addr:state'),
    ('postcode', 'addr:postcode'),
    ('country', 'addr:country'),
    ('name', 'name'),
    ('phone', 'phones'),
    ('email', 'email'),
    ('website', 'website'),
    ('store_url', 'store_url'),
    ('opening_hours', 'operatingHours'),
    ('brand', 'brand'),
    ('chain_id', 'chain_id'),
    ('chain_name', 'chain_name'),
    ('categories', 'categories'),
    ('brand_wikidata', 'brand:wikidata'),
)

def convert_category(category_name):
    return {
        "type": category_name,
        "langCode": "en"
    }

def convert_attrs(attribute_type, attribute_value):
    if attribute_type == "phone":
        if attribute_value:
            return { "Store": attribute_value }
        else:
            return { "Store": [] }
    
    elif attribute_type == "email":
        if attribute_value:
            return { "Customer Service": attribute_value }
        else:
            return { "Customer Service": [] }
    
    elif attribute_type == "opening_hours":
        if attribute_value:
            return { "Store": attribute_value }
        else:
            return { "Store": [] }
    
    elif attribute_type == "categories":
        if attribute_value:
            return [convert_category(category_name) for category_name in attribute_value]
        else:
            return []
    
    else:
        return attribute_value
  

def item_to_properties(item):
    props = {}

    # Ref is required
    props['ref'] = str(item['ref'])

    # Add in the extra bits
    extras = item.get('extras')
    if extras:
        props.update(extras)

    # Bring in the optional stuff
    for map_from, map_to in mapping:
        item_value = item.get(map_from)
        item_value = convert_attrs(map_from, item_value)
        
        if item_value:
            props[map_to] = item_value

    return props


def compute_hash(item):
    ref = str(item.get('ref') or '').encode('utf8')
    sha1 = hashlib.sha1(ref)

    spider_name = item.get('extras', {}).get('@spider')
    if spider_name:
        sha1.update(spider_name.encode('utf8'))

    return base64.urlsafe_b64encode(sha1.digest()).decode('utf8')


class LineDelimitedGeoJsonExporter(JsonLinesItemExporter):

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        feature = []
        feature.append(('type', 'Feature'))
        feature.append(('id', compute_hash(item)))
        feature.append(('properties', item_to_properties(item)))

        lat = item.get('lat')
        lon = item.get('lon')
        if lat and lon:
            try:
                feature.append(('geometry', {
                    'type': 'Point',
                    'coordinates': [
                        float(item['lon']),
                        float(item['lat'])
                    ],
                }))
            except ValueError:
                logging.warning("Couldn't convert lat (%s) and lon (%s) to string", lat, lon)
                pass

        return feature


class GeoJsonExporter(JsonItemExporter):

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        feature = []
        feature.append(('type', 'Feature'))
        feature.append(('id', compute_hash(item)))
        feature.append(('properties', item_to_properties(item)))

        lat = item.get('lat')
        lon = item.get('lon')
        if lat and lon:
            try:
                feature.append(('geometry', {
                    'type': 'Point',
                    'coordinates': [
                        float(item['lon']),
                        float(item['lat'])
                    ],
                }))
            except ValueError:
                logging.warning("Couldn't convert lat (%s) and lon (%s) to string", lat, lon)
                pass

        return feature

    def start_exporting(self):
        self.file.write(to_bytes('{"type":"FeatureCollection","features":[', self.encoding))

    def finish_exporting(self):
        self.file.write(to_bytes(']}', self.encoding))
