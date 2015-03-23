#-*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

ENERGY_CONSUMPTION_CHOICES = (
    ('A', _(u'A - ≤ 50')),
    ('B', _(u'B - 51 à 90')),
    ('C', _(u'C - 91 à 150')),
    ('D', _(u'D - 151 à 230')),
    ('E', _(u'E - 231 à 330')),
    ('F', _(u'F - 331 à 450')),
    ('G', _(u'G - > 450')),
)

EMISSION_OF_GREENHOUSE_GASES_CHOICES = (
    ('A', _(u'A - ≤ 5')),
    ('B', _(u'B - 6 à 10')),
    ('C', _(u'C - 11 à 20')),
    ('D', _(u'D - 21 à 35')),
    ('E', _(u'E - 36 à 55')),
    ('F', _(u'F - 56 à 80')),
    ('G', _(u'G - > 80')),
)

HEATING_CHOICES = (
    ('1', _(u'individuel gaz')),
    ('2', _(u'individuel électrique')),
    ('3', _(u'collectif gaz')),
    ('4', _(u'collectif fuel')),
    ('5', _(u'collectif réseau de chaleur')),
    ('13', _(u'autres'))
)


KITCHEN_CHOICES = (
    ('1', _(u'américaine')),
    ('2', _(u'séparée')),
    ('3', _(u'industrielle')),
    ('4', _(u'coin-cuisine')),
    ('5', _(u'belle vue')),
    ('6', _(u'sans vis à vis')),
    ('7', _(u'américaine équipée')),
    ('8', _(u'séparée équipée')),
    ('9', _(u'coin cuisine équipé')),
)


PARKING_CHOICES = (
    ('1', _(u'Place de parking')),
    ('2', _(u'Box fermé')),
)

FIREPLACE_CHOICES = (
    ('1', _(u'Foyer ouvert')),
    ('2', _(u'Insert')),
)
