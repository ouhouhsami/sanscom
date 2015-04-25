#-*- coding: utf-8 -*-
from PIL import Image

from django.db import models
from django.db.models import Q
from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.utils.translation import ugettext as _

from django_extensions.db.fields import AutoSlugField

from jsonfield import JSONField

from ads.utils import geo_from_address, json_from_address

from .abstract import BaseModel
from .choices import ENERGY_CONSUMPTION_CHOICES, EMISSION_OF_GREENHOUSE_GASES_CHOICES, HEATING_CHOICES, FIREPLACE_CHOICES, PARKING_CHOICES


class HabitationType(models.Model):
    label = models.CharField(max_length=25)

    def __unicode__(self):
        return self.label

    class Meta:
        db_table = 'ads_habitationtype'
        app_label = 'ads'


class AdManager(models.GeoManager):
    def get_queryset(self):
        return super(AdManager, self).get_queryset().filter(valid=True).select_related('habitation_type').prefetch_related('adpicture_set')


class ModerationAdManager(models.GeoManager):
    def get_queryset(self):
        return super(AdManager, self).get_queryset().select_related('habitation_type').prefetch_related('adpicture_set')


class Ad(BaseModel):
    """
    Ad model
    """
    slug = AutoSlugField(_('slug'), populate_from='slug_format')
    location = models.PointField(u"Localisation")
    address = models.CharField(_(u"Adresse"), max_length=255)
    json_address = JSONField()
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

    objects = AdManager()
    included_not_validated_objects = ModerationAdManager()

    @models.permalink
    def get_absolute_url(self):
        return ('%s:ads_ad_detail' % self.transaction, [str(self.slug)])

    def save(self, *args, **kwargs):
        self.location = geo_from_address(self.address)
        self.json_address = json_from_address(self.address)
        super(Ad, self).save(*args, **kwargs)

    def _get_slug_format(self):
        return u'%s-%se-%sm²' % (self.habitation_type.label, self.price, self.surface)
    slug_format = property(_get_slug_format)

    def _get_search_query(self):
        return '?price_max=%s&surface_min=%s&location=%s' % (self.price, self.surface, geos.MultiPolygon(self.location.buffer(0.015)))
    search_query = property(_get_search_query)

    @property
    def interested_count(self):
        return self.interested.count()

    @property
    def contacted_count(self):
        return self.contacted.count()

    @property
    def approached_count(self):
        return self.approached.count()

    @property
    def interested(self):
        return self.adsearchrelation_set.all().filter(valid=True)

    @property
    def contacted(self):
        return self.adsearchrelation_set.all().filter(valid=True).filter(search_contacted__isnull=False)

    @property
    def approached(self):
        return self.adsearchrelation_set.all().filter(valid=True).filter(ad_contacted__isnull=False)

    @property
    def no_contacts(self):
        return self.adsearchrelation_set.all().filter(valid=True).filter(ad_contacted__isnull=True).filter(search_contacted__isnull=True)

    @property
    def contacts(self):
        return self.adsearchrelation_set.all().filter(valid=True).filter(Q(ad_contacted__isnull=False) | Q(search_contacted__isnull=False))

    @property
    def district(self):
        try:
            address_components = self.json_address['results'][0]['address_components']
            for component in address_components:
                if "locality" in component["types"]:
                    locality = component["long_name"]
                if "postal_code" in component["types"]:
                    postal_code = component["long_name"]
            if locality and postal_code:
                return u"%s, %s" % (locality, postal_code)
            else:
                return False
        except:
            return False

    @property
    def locality(self):
        try:
            address_components = self.json_address['results'][0]['address_components']
            for component in address_components:
                if "locality" in component["types"]:
                    locality = component["long_name"]
            if locality:
                return u"%s" % locality
            else:
                return False
        except:
            return False

    @property
    def square_meter_price(self):
        return self.price / self.surface

    def __unicode__(self):
        unity = u'€'
        if self.transaction == 'rent':
            unity = u'€/mois'
        return u'%s - %s %s - %s m²' % (self.habitation_type.label, self.price, unity, self.surface)

    class Meta:
        db_table = 'ads_ad'
        app_label = 'ads'


class AdPicture(models.Model):
    """
    Ad Picture model
    """
    ad = models.ForeignKey(Ad)
    image = models.ImageField("Photo", upload_to="pictures/%Y/%m/%d")
    title = models.CharField("Titre", max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(AdPicture, self).save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            image.thumbnail((680, 510), Image.NEAREST)
            image.save(self.image.path)

    class Meta:
        db_table = 'ads_adpicture'
        app_label = 'ads'
