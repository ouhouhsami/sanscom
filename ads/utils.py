#-*- coding: utf-8 -*-
import requests
from django.conf import settings

#KEY_API = 'AIzaSyDybLZ5Wudjcjumgn8sZH9T3ko9FtOwduw'
GOOGLE_KEY_API = settings.GOOGLE_KEY_API


class WrongAddressError(Exception):
    pass


def geo_from_address(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true&key=%s" % (address, GOOGLE_KEY_API)
    #url = "http://nominatim.openstreetmap.org/search?q=%s&format=json" % address
    r = requests.get(url)
    try:
        json = r.json()
        #lng = json[0]['lon']
        #lat = json[0]['lat']
        lat = json['results'][0]['geometry']['location']['lat']
        lng = json['results'][0]['geometry']['location']['lng']
        pt = "POINT(%s %s)" % (lng, lat)
        return pt
    except IndexError:
        raise WrongAddressError


def json_from_address(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true&key=%s" % (address, GOOGLE_KEY_API)
    r = requests.get(url)
    try:
        json = r.json()
        return json
    except:
        raise WrongAddressError


def address_from_geo(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=true&key=%s" % (lat, lng, GOOGLE_KEY_API)
    #url = "http://nominatim.openstreetmap.org/reverse?format=json&lat=%s&lon=%s" % (lat, lng)
    r = requests.get(url)
    try:
        json = r.json()
        address = json['results'][0]['formatted_address']
        #address = json['display_name']
        #print address
        return address
    except IndexError:
        #print 'wrong'
        raise WrongAddressError
