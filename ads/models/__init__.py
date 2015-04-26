#-*- coding: utf-8 -*-
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Q

from .ad import Ad, AdPicture, HabitationType
from .search import Search
from .relation import AdSearchRelation
from .choices import *


def update_adsearch_relation_from_ad(sender, instance, **kwargs):
    ad = instance
    # @todo: seems like for required field in search, Q(price_max=None)
    # Q(surface_min=None), Q(habitation_types=None) and
    # Q(location__contains=ad.location) are useless
    # but they are usefull for rooms_min, which is not required param
    s = Search.objects\
            .filter(transaction=ad.transaction)\
            .filter(Q(price_max__gte=ad.price) | Q(price_max=None))\
            .filter(Q(surface_min__lte=ad.surface) | Q(surface_min=None))\
            .filter(Q(habitation_types=ad.habitation_type) | Q(habitation_types=None))\
            .filter(Q(location__contains=ad.location) | Q(location=None))\
            .filter(Q(rooms_min__lte=ad.rooms) | Q(rooms_min=None))\
            .filter(Q(ground_floor=ad.ground_floor) | Q(ground_floor=None))\
            .filter(Q(top_floor=ad.top_floor) | Q(top_floor=None))\
            .filter(Q(not_overlooked=ad.not_overlooked) | Q(not_overlooked=None))\
            .filter(Q(elevator=ad.elevator) | Q(elevator=None))\
            .filter(Q(intercom=ad.intercom) | Q(intercom=None))\
            .filter(Q(digicode=ad.digicode) | Q(digicode=None))\
            .filter(Q(doorman=ad.doorman) | Q(doorman=None))\
            .filter(Q(kitchen=ad.kitchen) | Q(kitchen=None))\
            .filter(Q(duplex=ad.duplex) | Q(duplex=None))\
            .filter(Q(swimming_pool=ad.swimming_pool) | Q(swimming_pool=None))\
            .filter(Q(alarm=ad.alarm) | Q(alarm=None))\
            .filter(Q(air_conditioning=ad.air_conditioning) | Q(air_conditioning=None))\
            .filter(Q(fireplace=ad.fireplace) | Q(fireplace=None))\
            .filter(Q(terrace=ad.terrace) | Q(terrace=None))\
            .filter(Q(balcony=ad.balcony) | Q(balcony=None))\
            .filter(Q(separate_dining_room=ad.separate_dining_room) | Q(separate_dining_room=None))\
            .filter(Q(separate_toilet=ad.separate_toilet) | Q(separate_toilet=None))\
            .filter(Q(bathroom=ad.bathroom) | Q(bathroom=None))\
            .filter(Q(shower=ad.shower) | Q(shower=None))\
            .filter(Q(separate_entrance=ad.separate_entrance) | Q(separate_entrance=None))\
            .filter(Q(cellar=ad.cellar) | Q(cellar=None))\
            .filter(Q(parking=ad.parking) | Q(parking=None))
    if ad.bedrooms:
        s = s.filter(Q(bedrooms_min__lte=ad.bedrooms) | Q(bedrooms_min__isnull=True))
    if ad.ground_surface:
        s = s.filter(Q(ground_surface_min__lte=ad.ground_surface) | Q(ground_surface_min__isnull=True))
            #.filter(Q(price__min__lte=ad.price) | Q(price__min=None))\
            #.filter(Q(surface_max__gte=ad.surface) | Q(surface_max=None))\
            #.filter(Q(rooms_max__gte=ad.rooms) | Q(rooms_max=None))\
            #.filter(Q(bedrooms_min__lte=ad.bedrooms) | Q(bedrooms_min=None))\
            #.filter(Q(bedrooms_max__gte=ad.bedrooms) | Q(bedrooms_max=None))\

    asr_search = Search.objects.filter(adsearchrelation__ad=ad)
    # Search in s and not in asr_search => add
    for search in s:
        if search not in asr_search:
            a = AdSearchRelation(ad=ad, search=search, valid=True)
            a.moderated = ad.valid and search.valid
            a.save()
    # Search in s and in asr_search => nothing
    for search in asr_search:
        if search in s:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.valid = True
            a.moderated = ad.valid and search.valid
            a.save()
        else:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.valid = False
            a.moderated = ad.valid and search.valid
            a.save()


def update_adsearch_relation_from_search(sender, instance, **kwargs):
    search = instance
    q_ad = Ad.objects.all().filter(price__lte=search.price_max)\
                           .filter(surface__gte=search.surface_min)\
                           .filter(habitation_type__in=search.habitation_types.all())\
                           .filter(location__within=search.location)\
                           .filter(transaction=search.transaction)
    if search.rooms_min:
            q_ad = q_ad.filter(rooms__gte=search.rooms_min)
    if search.bedrooms_min:
            q_ad = q_ad.filter(bedrooms__gte=search.bedrooms_min)
    if search.ground_surface_min:
            q_ad = q_ad.filter(ground_surface__gte=search.ground_surface_min)
    if search.ground_floor:
            q_ad = q_ad.filter(ground_floor=search.ground_floor)
    if search.top_floor:
            q_ad = q_ad.filter(top_floor=search.top_floor)
    if search.not_overlooked:
            q_ad = q_ad.filter(not_overlooked=search.not_overlooked)
    if search.elevator:
            q_ad = q_ad.filter(elevator=search.elevator)
    if search.intercom:
            q_ad = q_ad.filter(intercom=search.intercom)
    if search.digicode:
            q_ad = q_ad.filter(digicode=search.digicode)
    if search.doorman:
            q_ad = q_ad.filter(doorman=search.doorman)
    if search.kitchen:
            q_ad = q_ad.filter(kitchen=search.kitchen)
    if search.duplex:
            q_ad = q_ad.filter(duplex=search.duplex)
    if search.swimming_pool:
            q_ad = q_ad.filter(swimming_pool=search.swimming_pool)
    if search.alarm:
            q_ad = q_ad.filter(alarm=search.alarm)
    if search.air_conditioning:
            q_ad = q_ad.filter(air_conditioning=search.air_conditioning)
    if search.fireplace:
            q_ad = q_ad.filter(fireplace=search.fireplace)
    if search.terrace:
            q_ad = q_ad.filter(terrace=search.terrace)
    if search.balcony:
            q_ad = q_ad.filter(balcony=search.balcony)
    if search.separate_dining_room:
            q_ad = q_ad.filter(separate_dining_room=search.separate_dining_room)
    if search.separate_toilet:
            q_ad = q_ad.filter(separate_toilet=search.separate_toilet)
    if search.bathroom:
            q_ad = q_ad.filter(bathroom=search.bathroom)
    if search.shower:
            q_ad = q_ad.filter(shower=search.shower)
    if search.separate_entrance:
            q_ad = q_ad.filter(separate_entrance=search.separate_entrance)
    if search.cellar:
            q_ad = q_ad.filter(cellar=search.cellar)
    if search.parking:
            q_ad = q_ad.filter(parking=search.parking)

    asr_ad = Ad.objects.filter(adsearchrelation__search=search)
    for ad in asr_ad:
        if ad not in q_ad:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.moderated = ad.valid and search.valid
            a.valid = False
        else:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.moderated = ad.valid and search.valid
            a.valid = True
        a.save()
    for ad in q_ad:
        if ad not in asr_ad:
            a, create = AdSearchRelation.objects.get_or_create(ad=ad, search=search)
            a.valid = True
            a.moderated = ad.valid and search.valid
            a.save()


post_save.connect(update_adsearch_relation_from_ad, sender=Ad)
post_save.connect(update_adsearch_relation_from_search, sender=Search)
m2m_changed.connect(update_adsearch_relation_from_search, sender=Search.habitation_types.through)
