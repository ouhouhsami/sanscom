#-*- coding: utf-8 -*-

from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage
from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.db.models.signals import post_save, m2m_changed
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from django.utils.translation import ugettext as _

from .utils import geo_from_address


class BaseModel(TimeStampedModel):
    description = models.TextField(_('description'), blank=True, null=True)
    user = models.ForeignKey(User)

    class Meta:
        abstract = True


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


class HabitationType(models.Model):
    label = models.CharField(max_length=25)

    def __unicode__(self):
        return self.label


class Ad(BaseModel):
    """
    Ad model
    """
    slug = AutoSlugField(_('slug'), populate_from='slug_format')
    location = models.PointField(u"Localisation")
    address = models.CharField(_(u"Adresse"), max_length=255)
    price = models.PositiveIntegerField(_(u"Prix"))
    habitation_type = models.ForeignKey(HabitationType, verbose_name="Type de bien")
    surface = models.IntegerField(_(u"Surface habitable"))
    surface_carrez = models.IntegerField(_(u"Surface Loi Carrez"),
                                         null=True, blank=True)
    rooms = models.PositiveIntegerField(_(u"Nombre de pièces"))
    bedrooms = models.PositiveIntegerField(_(u"Nombre de chambres"))
    energy_consumption = models.CharField(_(u"Consommation énergétique (kWhEP/m².an)"),
                                          max_length=1,
                                          choices=ENERGY_CONSUMPTION_CHOICES,
                                          null=True, blank=True)
    ad_valorem_tax = models.IntegerField(_(u'Taxe foncière'), null=True,
                                         blank=True,
                                         help_text=_(u"Montant annuel, sans espace, sans virgule"))
    housing_tax = models.IntegerField(_(u"Taxe d'habitation"), null=True,
                                      blank=True, help_text=_(u"Montant annuel, sans espace, sans virgule"))
    maintenance_charges = models.IntegerField(_(u'Charges'), null=True,
                                              blank=True, help_text=_(u"Montant mensuel, sans espace, sans virgule"))
    emission_of_greenhouse_gases = models.CharField(_(u"Émissions de gaz à effet de serre (kgeqCO2/m².an)"),
                                                    max_length=1,
                                                    choices=EMISSION_OF_GREENHOUSE_GASES_CHOICES,
                                                    null=True, blank=True)
    ground_surface = models.IntegerField(_(u'Surface du terrain'),
                                       null=True, blank=True)
    floor = models.PositiveIntegerField(_(u'Etage'), null=True, blank=True)
    ground_floor = models.BooleanField(_(u'Rez de chaussé'), default=False)
    top_floor = models.BooleanField(_(u'Dernier étage'), default=False)
    not_overlooked = models.BooleanField(_(u'Sans vis-à-vis'), default=False)
    elevator = models.BooleanField(_(u"Ascenceur"), default=False)
    intercom = models.BooleanField(_(u"Interphone"), default=False)
    digicode = models.BooleanField(_(u"Digicode"), default=False)
    doorman = models.BooleanField(_(u"Gardien"), default=False)
    heating = models.CharField(_(u"Chauffage"), max_length=2,
                               choices=HEATING_CHOICES, null=True, blank=True)
    kitchen = models.BooleanField(_(u"Cuisine équipée"), default=False)
    duplex = models.BooleanField(_(u"Duplex"), default=False)
    swimming_pool = models.BooleanField(_(u"Piscine"), default=False)
    alarm = models.BooleanField(_(u"Alarme"), default=False)
    air_conditioning = models.BooleanField(_(u"Climatisation"), default=False)
    fireplace = models.CharField(_(u"Cheminée"), max_length=2,
                               choices=FIREPLACE_CHOICES, null=True, blank=True)
    terrace = models.IntegerField(_(u"Terrasse"), null=True, blank=True)
    balcony = models.IntegerField(_(u"Balcon"), null=True, blank=True)
    separate_dining_room = models.BooleanField(_(u"Cuisine séparée"), default=False)
    separate_toilet = models.IntegerField(_(u"Toilettes séparés"), null=True, blank=True)
    bathroom = models.IntegerField(_(u"Salle de bain"), null=True, blank=True)
    shower = models.IntegerField(_(u"Salle d'eau (douche)"), null=True, blank=True)
    separate_entrance = models.BooleanField(_(u"Entrée séparée"), default=False)
    cellar = models.BooleanField(_(u"Cave"), default=False)
    parking = models.CharField(_(u"Parking"), max_length=2,
                               choices=PARKING_CHOICES, null=True, blank=True)
    orientation = models.CharField(_(u"Orientation"), max_length=255, null=True, blank=True)

    objects = models.GeoManager()

    @models.permalink
    def get_absolute_url(self):
        return ('ads_ad_detail', [str(self.slug)])

    def save(self, *args, **kwargs):
        self.location = geo_from_address(self.address)
        super(Ad, self).save(*args, **kwargs)

    def _get_slug_format(self):
        return u'%s-%se-%sm²' % (self.habitation_type.label, self.price, self.surface)
    slug_format = property(_get_slug_format)


    def _get_search_query(self):
        return '?price_max=%s&surface_min=%s&location=%s' % (self.price, self.surface, geos.MultiPolygon(self.location.buffer(0.015)))

    search_query = property(_get_search_query)

    def __unicode__(self):
        return u'%s - %s € - %s m²' % (self.habitation_type.label, self.price, self.surface)


class AdPicture(models.Model):
    """
    Ad Picture model
    """
    ad = models.ForeignKey(Ad)
    image = models.ImageField("Photo", upload_to="pictures/%Y/%m/%d")
    title = models.CharField("Titre", max_length=255, null=True, blank=True)


NULL_CHOICES = (
    (None, _(u'Indifférent')),
    (True, _('Oui')),
    (False, _('Non'))
)


class IndifferentBooleanField(models.NullBooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = NULL_CHOICES
        super(IndifferentBooleanField, self).__init__(*args, **kwargs)


class Search(BaseModel):
    """
    Search model
    """
    slug = AutoSlugField(_('slug'), populate_from='slug_format')
    location = models.MultiPolygonField(_(u"Localisation"))
    price_max = models.PositiveIntegerField(_(u"Prix maximum"))
    habitation_types = models.ManyToManyField(HabitationType, verbose_name=u"Types d'habitations")
    surface_min = models.PositiveIntegerField(_(u"Surface minimale"))
    rooms_min = models.PositiveIntegerField(_(u"Nombre de pièces minimum"), null=True, blank=True)

    bedrooms_min = models.PositiveIntegerField(_(u"Nombre de chambres minimum"), null=True, blank=True)
    ground_surface_min = models.IntegerField(_(u'Surface du terrain minimale'), null=True, blank=True)
    ground_floor = IndifferentBooleanField(_(u'Rez de chaussé'), blank=True, default=None)
    top_floor = IndifferentBooleanField(_(u'Dernier étage'), blank=True)
    not_overlooked = IndifferentBooleanField(_(u'Sans vis-à-vis'), blank=True)
    elevator = IndifferentBooleanField(_(u"Ascenceur"), blank=True)
    intercom = IndifferentBooleanField(_(u"Interphone"), blank=True)
    digicode = IndifferentBooleanField(_(u"Digicode"), blank=True)
    doorman = IndifferentBooleanField(_(u"Gardien"), blank=True)
    kitchen = IndifferentBooleanField(_(u"Cuisine équipée"), blank=True)
    duplex = IndifferentBooleanField(_(u"Duplex"), blank=True)
    swimming_pool = IndifferentBooleanField(_(u"Piscine"), blank=True)
    alarm = IndifferentBooleanField(_(u"Alarme"), blank=True)
    air_conditioning = IndifferentBooleanField(_(u"Climatisation"), blank=True)
    fireplace = IndifferentBooleanField(_(u"Cheminée"), blank=True)
    terrace = IndifferentBooleanField(_(u"Terrasse"), blank=True)
    balcony = IndifferentBooleanField(_(u"Balcon"), blank=True)
    separate_dining_room = IndifferentBooleanField(_(u"Cuisine séparée"), blank=True)
    separate_toilet = IndifferentBooleanField(_(u"Toilettes séparés"), blank=True)
    bathroom = IndifferentBooleanField(_(u"Salle de bain"), blank=True)
    shower = IndifferentBooleanField(_(u"Salle d'eau (douche)"), blank=True)
    separate_entrance = IndifferentBooleanField(_(u"Entrée séparée"), blank=True)
    cellar = IndifferentBooleanField(_(u"Cave"), blank=True)
    parking = IndifferentBooleanField(_(u"Parking"), blank=True)

    #floor_min = models.PositiveIntegerField(_(u'Etage minimal'), null=True, blank=True)
    #floor_max = models.PositiveIntegerField(_(u'Etage maximal'), null=True, blank=True)
    #energy_consumption_min = models.CharField(_(u"Consommation énergétique (kWhEP/m².an) minimale"),
    #                                      max_length=1,
    #                                      choices=ENERGY_CONSUMPTION_CHOICES,
    #                                      null=True, blank=True)
    #ad_valorem_tax_max = models.IntegerField(_(u'Taxe foncière maximum'), null=True,
    #                                     blank=True,
    #                                     help_text=_(u"Montant annuel maximum, sans espace, sans virgule"))
    #housing_tax_max = models.IntegerField(_(u"Taxe d'habitation maximum"), null=True,
    #                                  blank=True, help_text=_(u"Montant annuel maximum, sans espace, sans virgule"))
    #maintenance_charges_max = models.IntegerField(_(u'Charges maximum'), null=True,
    #                                          blank=True, help_text=_(u"Montant mensuel maximum, sans espace, sans virgule"))
    #emission_of_greenhouse_gases_min = models.CharField(_(u"Émissions de gaz à effet de serre (kgeqCO2/m².an) minimales"),
    #                                                max_length=1,
    #                                                choices=EMISSION_OF_GREENHOUSE_GASES_CHOICES,
    #                                                null=True, blank=True)

    objects = models.GeoManager()

    @models.permalink
    def get_absolute_url(self):
        return ('ads_search_detail', [str(self.slug)])

    def _get_slug_format(self):
        return u'%se-max-%sm²-min' % (self.price_max, self.surface_min)
    slug_format = property(_get_slug_format)

    def __unicode__(self):
        return u'%s - %s € max. - %s m² min.' % (', '.join(self.habitation_types.all().values_list('label', flat=True)), self.price_max, self.surface_min)


class AdSearchRelationManager(models.Manager):
    def get_queryset(self):
        return super(AdSearchRelationManager, self).get_queryset().filter(valid=True)


class AdSearchRelation(TimeStampedModel):
    """
    Ad Search model Relation
    """
    ad = models.ForeignKey(Ad)
    search = models.ForeignKey(Search)
    ad_notified = models.DateTimeField(null=True, blank=True)
    search_notified = models.DateTimeField(null=True, blank=True)
    ad_contacted = models.DateTimeField(null=True, blank=True)
    search_contacted =  models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=False)

    valid_objects = AdSearchRelationManager()
    objects = models.Manager()

    def has_vendor_contacted_buyer_for_search(self, vendor, search):
        pass

    def has_buyer_contacted_vendor_for_ad(self, buyer, ad):
        pass

    class Meta:
        unique_together = (('ad', 'search'), )


    def save(self, *args, **kwargs):
        if self.valid:
            if self.ad_notified is None and self.search_notified is None:
                # Go for a mail, because ASR is valid and ad and search owner haven't been notifided yet.
                self.ad_notified = timezone.now()
                self.search_notified = timezone.now()
                # Mail to ad owner
                ad_full_url = u''.join(['http://', get_current_site(None).domain, self.ad.get_absolute_url()])
                search_full_url = u''.join(['http://', get_current_site(None).domain, self.search.get_absolute_url()])
                message = u'''Bonjour,
                \n\nUn nouvel acheteur potentiel pour votre bien, consultez sa recherche : %s .
                \n\nA bientôt
                \n\nL'équipe AcheterSansCom
                ''' % search_full_url
                sender = "contact@acheternsanscom.com"
                recipients = [self.ad.user.email, ]
                subject = "[AcheterSansCom] Un nouvel acheteur potentiel pour votre bien - %s" % self.ad
                mail = EmailMessage(subject, message, sender, recipients, [sender])
                mail.send()
                # Mail to search owner
                message = u'''Bonjour,
                \n\nUn nouveau bien correspond à votre recherche : %s .
                \n\nA bientôt
                \n\nL'équipe AcheterSansCom
                ''' % ad_full_url
                sender = "contact@acheternsanscom.com"
                recipients = [self.search.user.email, ]
                subject = "[AcheterSansCom] Un nouveau bien correspondant à votre recherche - %s" % self.search
                mail = EmailMessage(subject, message, sender, recipients, [sender])
                mail.send()
        super(AdSearchRelation, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"ad: %s | search: %s | valid: %s" % (self.ad, self.search, self.valid)


def update_adsearch_relation_from_ad(sender, instance, **kwargs):
    ad = instance
    # @todo: seems like for required field in search, Q(price_max=None)
    # Q(surface_min=None), Q(habitation_types=None) and
    # Q(location__contains=ad.location) are useless
    # but they are usefull for rooms_min, which is not required param
    s = Search.objects\
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

    asr = AdSearchRelation.objects.filter(ad=ad).values_list('search', flat=True)
    # Search in s and not in asr => add
    for search in s:
        if search not in asr:
            a = AdSearchRelation(ad=ad, search=search, valid=True)
            a.save()
    # Search in s and in asr => nothing
    for search in asr:
        if search in s:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.valid = True
            a.save()
        else:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.valid = False
            a.save()


def update_adsearch_relation_from_search(sender, instance, **kwargs):
    search = instance
    q_ad = Ad.objects.all().filter(price__lte=search.price_max)\
                           .filter(surface__gte=search.surface_min)\
                           .filter(habitation_type__in=search.habitation_types.all())\
                           .filter(location__within=search.location)
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

    asr = AdSearchRelation.objects.filter(search=search).values_list('ad', flat=True)
    for ad in asr:
        if ad not in q_ad:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.valid = False
        else:
            a = AdSearchRelation.objects.get(ad=ad, search=search)
            a.valid = True
        a.save()
    for ad in q_ad:
        if ad not in asr:
            a, create = AdSearchRelation.objects.get_or_create(ad=ad, search=search)
            a.valid = True
            a.save()


post_save.connect(update_adsearch_relation_from_ad, sender=Ad)
post_save.connect(update_adsearch_relation_from_search, sender=Search)

m2m_changed.connect(update_adsearch_relation_from_search, sender=Search.habitation_types.through)
