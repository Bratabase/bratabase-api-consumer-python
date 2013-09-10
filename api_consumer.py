#!/usr/bin/env python
# coding: utf-8

import json
from urllib2 import urlopen


BRATABASE_API = 'https://api.bratabase.com/v0/'


def get_top_brands(endpoint):
    # GET to the API endpoint
    request = urlopen(endpoint)
    # Read the contents which are a JSON string
    json_data = request.read()
    # Convert to Python structure
    root = json.loads(json_data)
    brands_url = root['links']['brands']
    request = urlopen(brands_url)
    json_data = request.read()
    brands_collection = json.loads(json_data)
    top_brands = brands_collection['collection']
    return top_brands


def show_top_brands(brands):
    print '\n'.join(b['name'] for b in brands)


def ask_for_brand(brands):
    selected_brand = ''
    brand_names = [b['name'].lower() for b in brands]
    while selected_brand.lower() not in brand_names:
        selected_brand = raw_input('Type the name of a brand: ')

    for brand in brands:
        if brand['name'].lower() == selected_brand.lower():
            return brand


def follow_brand(brand):
    brand_url = brand['href']
    request = urlopen(brand_url)
    json_data = request.read()
    brand_detail = json.loads(json_data)
    models_url = brand_detail['links']['models']
    request = urlopen(models_url)
    json_data = request.read()
    models_collection = json.loads(json_data)
    return models_collection['collection']


def show_top_models(models):
    print '\n'.join(m['name'] for m in models)


def show_welcome_screen():
    welcome = """This script will show you how to traverse the Bratabase API"""
    print welcome


def start(endpoint):
    show_welcome_screen()
    brands = get_top_brands(endpoint)
    show_top_brands(brands)
    selected_brand = ask_for_brand(brands)
    models = follow_brand(selected_brand)
    show_top_models(models)


if __name__ == '__main__':
    start(BRATABASE_API)
