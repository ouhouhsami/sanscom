#-*- coding: utf-8 -*-
import numpy as np
from random import randint, random

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.webdesign.lorem_ipsum import paragraphs

import factory
from factory.fuzzy import *
from ads.models import ENERGY_CONSUMPTION_CHOICES, EMISSION_OF_GREENHOUSE_GASES_CHOICES, HEATING_CHOICES, KITCHEN_CHOICES, PARKING_CHOICES, FIREPLACE_CHOICES, HabitationType

from accounts.models import UserProfile

from .utils import address_from_geo, WrongAddressError
from .models import BaseModel, Ad, Search, AdPicture


FUZZY_ENERGY_CONSUMPTION_CHOICES = dict(ENERGY_CONSUMPTION_CHOICES).keys()
FUZZY_EMISSION_OF_GREENHOUSE_GASES_CHOICES = dict(EMISSION_OF_GREENHOUSE_GASES_CHOICES).keys()
FUZZY_HEATING_CHOICES = dict(HEATING_CHOICES).keys()
FUZZY_KITCHEN_CHOICES = dict(KITCHEN_CHOICES).keys()
FUZZY_PARKING_CHOICES = dict(PARKING_CHOICES).keys()
FUZZY_FIREPLACE_CHOICES = dict(FIREPLACE_CHOICES).keys()

house = HabitationType.objects.get(label="Maison")
apartment = HabitationType.objects.get(label="Appartement")

# Around Paris
TOP = 48.89
RIGHT = 2.45
BOTTOM = 48.79
LEFT = 2.21


class FuzzyPoint(FuzzyText):
    def fuzz(self):
        return 'POINT (' + '%s %s' % (random.uniform(LEFT, RIGHT), random.uniform(TOP, BOTTOM)) + ')'


class FuzzyAddress(FuzzyText):
    def fuzz(self):
        address = ''
        while True:
            try:
                lng = random.uniform(LEFT, RIGHT)
                lat = random.uniform(TOP, BOTTOM)
                address = address_from_geo(lat, lng)
            except WrongAddressError:
                continue
            break
        return address


class FuzzyMultiPolygon(FuzzyText):
    def fuzz(self):
        top = random.uniform(TOP, BOTTOM)
        bottom = random.uniform(top, BOTTOM)
        left = random.uniform(LEFT, RIGHT)
        right = random.uniform(left, RIGHT)
        pos = {'top': top, 'left': left, 'bottom': bottom, 'right': right}
        return 'MULTIPOLYGON (((%(left)s %(top)s, %(left)s %(bottom)s, %(right)s %(bottom)s, %(right)s %(top)s, %(left)s %(top)s)))' % pos


class FuzzyRooms(BaseFuzzyAttribute):
    def fuzz(self):
        arr = np.array([0.23, 0.56, 0.79, 0.92])
        val = random.random()
        return (np.abs(arr-val)).argmin()+1


def address(ad):
    pt = GEOSGeometry(ad.location)
    lat = pt.y
    lng = pt.x
    return address_from_geo(lat, lng)


def surface_from_surface_carrez(ad):
    if bool(random.getrandbits(1)):
        return ad.surface_carrez
    else:
        return int(ad.surface_carrez+random.uniform(0.01, 0.3)*ad.surface_carrez)


def surface_carrez_from_rooms(ad):
    arr = [[8, 32], [25, 52], [42, 80], [55, 100], [70, 125]]
    return random.randint(*arr[ad.rooms-1])


def surface_from_rooms_min(search):
    arr = [[5, 35, 5], [25, 55, 5], [45, 85, 5], [55, 100, 5], [70, 125, 5]]
    return random.randrange(*arr[search.rooms_min-1])


def ground_surface_from_type(ad):
    if ad.habitation_type == house:
        random.randint(0, 3000)


def bathroom_number(ad):
    if ad.rooms == 1:
        return random.randint(0, 1)
    else:
        return 1


def shower_number(ad):
    if ad.rooms == 1:
        if ad.bathroom != 1:
            return random.randint(0, 1)
        else:
            return 0
    else:
        return random.randint(0, 1)


def parking_choice(ad):
    if random.random() > 0.2:
        return None
    else:
        return random.choice(['1', '2'])


def ad_valorem_tax(ad):
    if ad.transaction == 'rent':
        return None
    else:
        return random.randrange(100, 3000, 20)


def price(ad):
    p = int(ad.surface*randint(5362, 12857)/1000)*1000
    if ad.transaction == 'rent':
        p = p/500
    return p


def price_max(search):
    p = int(search.surface_min*randint(5362, 12857)/1000)*1000
    if search.transaction == 'rent':
        p = int(p/5000)*10
    return p


class AccountFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory('ads.factories.UserFactory', profile=None)
    phone = '666 667'


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "user%s" % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    #main_group = factory.SubFactory('ads.factories.AccountFactory')
    #profile = factory.RelatedFactory(AccountFactory, 'user')
    profile = factory.RelatedFactory(AccountFactory, 'user')

    @classmethod
    def _prepare(cls, create, password=None, **kwargs):
        return super(UserFactory, cls)._prepare(
            create,
            password=make_password(password),
            **kwargs
        )


class BaseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = BaseModel

    #description = FuzzyAttribute(paragraph)
    description = FuzzyAttribute(lambda: '\n'.join(paragraphs(2)))
    user = factory.SubFactory(UserFactory)
    transaction = FuzzyChoice(choices=['sale', 'rent'])
    valid = None


class HabitationTypeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = HabitationType

    label = factory.Sequence(lambda n: "label%s" % n)


class AdFactory(BaseFactory):
    """
    AdFactory
    Some data provided by http://www.cartesfrance.fr/Paris-75000/logement-Paris.html
    """
    FACTORY_FOR = Ad

    location = FuzzyPoint()
    address = factory.LazyAttribute(address)
    price = factory.LazyAttribute(price)
    habitation_type = factory.LazyAttribute(lambda i: house if random.random() < 0.009 else apartment)
    surface = factory.LazyAttribute(surface_from_surface_carrez)
    surface_carrez = factory.LazyAttribute(surface_carrez_from_rooms)
    rooms = FuzzyRooms()
    bedrooms = factory.LazyAttribute(lambda o: 1 if o.rooms <= 2 else random.randint(1, o.rooms-1))
    energy_consumption = FuzzyChoice(choices=FUZZY_ENERGY_CONSUMPTION_CHOICES)
    ad_valorem_tax = factory.LazyAttribute(ad_valorem_tax)
    housing_tax = FuzzyInteger(100, 3000, 30)
    maintenance_charges = FuzzyInteger(50, 400, 10)
    emission_of_greenhouse_gases = FuzzyChoice(choices=FUZZY_EMISSION_OF_GREENHOUSE_GASES_CHOICES)
    ground_surface = factory.LazyAttribute(ground_surface_from_type)
    floor = FuzzyInteger(0, 15)
    ground_floor = factory.LazyAttribute(lambda o: True if o.floor == 0 else False)
    top_floor = factory.LazyAttribute(lambda o: True if random.random() < 0.018 else False)
    not_overlooked = factory.LazyAttribute(lambda o: True if random.random() < 0.08 else False)
    elevator = FuzzyChoice(choices=[True, False])
    intercom = FuzzyChoice(choices=[True, False])
    digicode = FuzzyChoice(choices=[True, False])
    doorman = factory.LazyAttribute(lambda o: True if random.random() < 0.3 else False)
    heating = FuzzyChoice(choices=FUZZY_HEATING_CHOICES)
    kitchen = FuzzyChoice(choices=[True, False])
    duplex = factory.LazyAttribute(lambda o: True if random.random() < 0.05 else False)
    swimming_pool = factory.LazyAttribute(lambda o: True if random.random() < 0.01 else False)
    alarm = factory.LazyAttribute(lambda o: True if random.random() < 0.05 else False)
    air_conditioning = factory.LazyAttribute(lambda o: True if random.random() < 0.02 else False)
    fireplace = FuzzyChoice(choices=FUZZY_FIREPLACE_CHOICES)
    terrace = factory.LazyAttribute(lambda o: random.randint(8, 50) if random.random() < 0.01 else None)
    balcony = factory.LazyAttribute(lambda o: random.randint(2, 20) if random.random() < 0.08 else None)
    separate_dining_room = factory.LazyAttribute(lambda o: True if o.rooms-o.bedrooms >= 1 else False)
    separate_toilet = factory.LazyAttribute(lambda o: 1 if random.random() < 0.15 else 0)
    bathroom = factory.LazyAttribute(bathroom_number)
    shower = factory.LazyAttribute(shower_number)
    separate_entrance = factory.LazyAttribute(lambda o: True if random.random() < 0.1 else False)
    cellar = factory.LazyAttribute(lambda o: True if random.random() < 0.2 else False)
    parking = factory.LazyAttribute(parking_choice)
    orientation = FuzzyChoice(choices=['', 'sud', 'sud-est', 'sud-ouest', 'nord', 'nord-ouest', 'nord-est'])


class FakeAddressAdFactory(AdFactory):
    address = '13 rue de Veirneuil, paris'


class AdPictureFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = AdPicture

    title = FuzzyChoice(choices=["Cuisine", "Chambre", "Salon", "Salle à manger"])
    image = factory.django.ImageField(color='blue', width=900, height=100)
    ad = factory.SubFactory(AdFactory)


class SearchFactory(BaseFactory):
    FACTORY_FOR = Search

    location = FuzzyMultiPolygon()
    price_max = factory.LazyAttribute(price_max)
    surface_min = factory.LazyAttribute(surface_from_rooms_min)
    rooms_min = FuzzyRooms()

    bedrooms_min = factory.LazyAttribute(lambda o: 1 if o.rooms_min <= 2 else random.randint(1, o.rooms_min-1))
    ground_surface_min = FuzzyChoice(choices=[None, ])
    ground_floor = FuzzyChoice(choices=[None, True, False])
    top_floor = FuzzyChoice(choices=[None, True, False])
    not_overlooked = FuzzyChoice(choices=[None, True, False])
    elevator = FuzzyChoice(choices=[None, True, False])
    intercom = FuzzyChoice(choices=[None, True, False])
    digicode = FuzzyChoice(choices=[None, True, False])
    doorman = FuzzyChoice(choices=[None, True, False])
    kitchen = FuzzyChoice(choices=[None, True, False])
    duplex = FuzzyChoice(choices=[None, True, False])
    swimming_pool = FuzzyChoice(choices=[None, True, False])
    alarm = FuzzyChoice(choices=[None, True, False])
    air_conditioning = FuzzyChoice(choices=[None, True, False])
    fireplace = FuzzyChoice(choices=[None, True, False])
    terrace = FuzzyChoice(choices=[None, True, False])
    balcony = FuzzyChoice(choices=[None, True, False])
    separate_dining_room = FuzzyChoice(choices=[None, True, False])
    separate_toilet = FuzzyChoice(choices=[None, True, False])
    bathroom = FuzzyChoice(choices=[None, True, False])
    shower = FuzzyChoice(choices=[None, True, False])
    separate_entrance = FuzzyChoice(choices=[None, True, False])
    cellar = FuzzyChoice(choices=[None, True, False])
    parking = FuzzyChoice(choices=[None, True, False])

    @factory.post_generation
    def habitation_types(self, create, extracted, **kwargs):
        #t = FuzzyChoice(choices=[house, apartment]).fuzz()
        #self.habitation_types.add(t)
        if not create:
            return
        if extracted:
            for habitation_type in extracted:
                self.habitation_types.add(habitation_type)
