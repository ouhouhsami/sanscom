#-*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from django_extensions.db.models import TimeStampedModel

TRANSACTION_CHOICES = (
    ('sale', _('Vente')),
    ('rent', _('Location'))
)


class BaseModel(TimeStampedModel):
    description = models.TextField(_('description'), blank=True, null=True)
    user = models.ForeignKey(User)
    transaction = models.CharField(choices=TRANSACTION_CHOICES, max_length=4)

    @property
    def sale(self):
        if self.transaction == 'sale':
            return True
        return False

    @property
    def rent(self):
        if self.transaction == 'rent':
            return True
        return False

    class Meta:
        abstract = True
