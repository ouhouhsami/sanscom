#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis import geos
from django_extensions.db.fields import AutoSlugField

from django.utils.translation import ugettext as _

from .abstract import BaseModel
from .ad import HabitationType


NULL_CHOICES = (
    (None, _(u'Indifférent')),
    (True, _('Oui')),
    (False, _('Non'))
)


class IndifferentBooleanField(models.NullBooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = NULL_CHOICES
        super(IndifferentBooleanField, self).__init__(*args, **kwargs)


class SearchManager(models.GeoManager):
    def get_queryset(self):
        return super(SearchManager, self).get_queryset().select_related('habitation_types')


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

    objects = SearchManager() #models.GeoManager()

    @models.permalink
    def get_absolute_url(self):
        return ('%s:ads_search_detail' % self.transaction, [str(self.slug)])

    def _get_slug_format(self):
        return u'%se-max-%sm²-min' % (self.price_max, self.surface_min)
    slug_format = property(_get_slug_format)

    def __unicode__(self):
        unity = u'€'
        if self.transaction == 'rent':
            unity = u'€/mois'
        return u'%s - %s %s max. - %s m² min.' % (', '.join(self.habitation_types.all().values_list('label', flat=True)), self.price_max, unity, self.surface_min)

    class Meta:
        db_table = 'ads_search'
        app_label= 'ads'
