#-*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage
from django.db import models
from django.contrib.gis.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils import timezone

from ad import Ad
from search import Search


class AdSearchRelationManager(models.Manager):
    def get_queryset(self):
        return super(AdSearchRelationManager, self).get_queryset().filter(valid=True, moderated=True)


class AdSearchRelation(TimeStampedModel):
    """
    Ad Search model Relation
    """
    ad = models.ForeignKey(Ad)
    search = models.ForeignKey(Search)
    ad_notified = models.DateTimeField(null=True, blank=True)
    search_notified = models.DateTimeField(null=True, blank=True)
    ad_contacted = models.DateTimeField(null=True, blank=True)
    search_contacted = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=False)
    moderated = models.BooleanField(default=False)

    valid_objects = AdSearchRelationManager()
    objects = models.Manager()

    def has_vendor_contacted_buyer_for_search(self, vendor, search):
        pass

    def has_buyer_contacted_vendor_for_ad(self, buyer, ad):
        pass

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
                \n\nUne personne est interessée par votre bien, consultez sa recherche : %s .
                \n\nÀ bientôt
                \n\nL'équipe AcheterSansCom
                ''' % (search_full_url)
                sender = "contact@acheternsanscom.com"
                recipients = [self.ad.user.email, ]
                subject = "[AcheterSansCom] Une personne interessée par votre bien - %s" % self.ad
                mail = EmailMessage(subject, message, sender, recipients, [sender])
                mail.send()
                # Mail to search owner
                message = u'''Bonjour,
                \n\nUn bien correspond à votre recherche : %s .
                \n\nÀ bientôt
                \n\nL'équipe AcheterSansCom
                ''' % (ad_full_url)
                sender = "contact@acheternsanscom.com"
                recipients = [self.search.user.email, ]
                subject = "[AcheterSansCom] Un bien correspond à votre recherche - %s" % self.search
                mail = EmailMessage(subject, message, sender, recipients, [sender])
                mail.send()
        super(AdSearchRelation, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"ad: %s | search: %s | valid: %s" % (self.ad, self.search, self.valid)

    class Meta:
        unique_together = (('ad', 'search'), )
        db_table = 'ads_adsearchrelation'
        app_label= 'ads'
