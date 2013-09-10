#!/usr/bin/env python
# coding: utf-8

import json
from urllib2 import urlopen


BRATABASE_API = 'https://api.bratabase.com/v0/'


def get_top_brands(endpoint):
    """
    This function starts visiting the root of the API and from there it visits
    the Brands collection.
    Since the Brand collection is sorted by number of bras and paginated.
    Just reading the first page will return the list of Top brands.
    """

    # First GET to the API endpoint
    request = urlopen(endpoint)

    # Read the contents which are a JSON string
    json_data = request.read()

    # Convert to Python structure, now `root` contains the API's root payload
    #{
    #    "self": "https://api.bratabase.com/v0/",
    #    "links": {
    #        "me": "https://api.bratabase.com/v0/me/",
    #        "brands": "https://api.bratabase.com/v0/brands/"
    #    }
    #}
    root = json.loads(json_data)

    # We discover the brands collection url under the `links` section:
    brands_url = root['links']['brands']

    # Now we have the URL where to get the brands from, we GET to that URL
    request = urlopen(brands_url)

    # Read the JSON data and convert it to Python structure
    json_data = request.read()

    # `brands_collection` will now hold the response of the URL:
    #   https://api.bratabase.com/v0/brands/
    #{
    #    "collection": [ … ],
    #    "self": "https://api.bratabase.com/v0/brands/",
    #    "meta": {
    #        "page_total": 20,
    #        "paginated": true,
    #        "next": "https://api.bratabase.com/v0/brands/?page=2",
    #        "current": "https://api.bratabase.com/v0/brands/",
    #        "collection_total": 683,
    #        "prev": null
    #    },
    #    "links": { },
    #    "rel": "collection"
    #}
    brands_collection = json.loads(json_data)

    # We are only interested in the `collection` part of the payload, where
    # the actual list of brands is.
    top_brands = brands_collection['collection']
    # And we return that list of brand items
    return top_brands


def show_top_brands(brands):
    """
    This function will print a list of the names of the brands received.
    """
    print '\n'.join(b['name'] for b in brands)


def ask_for_brand(brands):
    """
    Here we ask the user to type the name of one of the displayed brands
    and return that brand's item.
    """
    selected_brand = ''

    # First we build a list of all the names of the brands received.
    # We do this so we can check that the name entered exists on this list.
    brand_names = [b['name'].lower() for b in brands]

    # Then we ask the user to type the name of a valid brand.
    while selected_brand.lower() not in brand_names:
        selected_brand = raw_input('Type the name of a brand: ')

    # Once we have that name, we iterate over all the brands until we find
    # the entry typed.
    for brand in brands:
        if brand['name'].lower() == selected_brand.lower():
            # Once we found the match, we return that entry
            # Sample:
            #
            #{
            #    "bratabase_url": "http://www.bratabase.com/browse/freya/",
            #    "href": "https://api.bratabase.com/v0/brands/freya/",
            #    "name": "Freya"
            #}
            return brand


def follow_brand(brand):
    """
    This function will receive the brand that was selected by the user
    and will follow its detail URL in order to have more information about it.
    This will return the collection of the available models for it.
    """
    # We start discovering the brand's API url under the `href` key.
    brand_url = brand['href']

    # Then we GET that URL and convert the JSON data to a Python structure
    request = urlopen(brand_url)
    json_data = request.read()

    # Now `brand_detail` contains the full body of a brand
    # {
    #    "body": {
    #        "bratabase_url": "http://www.bratabase.com/browse/panache/",
    #        "bras": 2280,
    #        "name": "Panache",
    #        "slug": "panache"
    #    },
    #    "links": {
    #        "models": "https://api.bratabase.com/v0/brands/panache/models/"
    #    },
    #    "self": "https://api.bratabase.com/v0/brands/panache/",
    #    "collection": "https://api.bratabase.com/v0/brands/",
    #    "meta": { },
    #    "rel": "entity"
    # }
    brand_detail = json.loads(json_data)

    # We discover the URL for the brand's collection under the `links` key.
    models_url = brand_detail['links']['models']

    # Again, we fetch that URL and convert it to a Python structure
    request = urlopen(models_url)
    json_data = request.read()

    # Similar to the Brands collection, we will now have a collection of
    # models for this brand.
    models_collection = json.loads(json_data)
    # We are only interested in the actual collection, so we return that.
    return models_collection['collection']


def show_top_models(models):
    """
    Print a list of the received models
    """
    print '\n'.join(m['name'] for m in models)


def show_welcome_screen():
    welcome = """This script will show you how to traverse the Bratabase API"""
    print welcome


def start(endpoint):
    # Print an introductory text, nothing exciting here
    show_welcome_screen()

    # This function will go to the API endpoint and fetch the collection
    # of top brands.
    brands = get_top_brands(endpoint)

    # Once we receive the brands, we print the names
    show_top_brands(brands)
    # Then we ask the user to type in the name of one of the brands
    selected_brand = ask_for_brand(brands)
    # We follow to read the list of models of this brand
    models = follow_brand(selected_brand)
    # And print the m on screen
    show_top_models(models)


if __name__ == '__main__':
    start(BRATABASE_API)
