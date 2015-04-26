#-*- coding: utf-8 -*-
from leaflet.admin import LeafletGeoAdmin

from django import forms
from django.contrib import admin
from django.core.mail import EmailMessage

from .models import Ad, AdPicture, Search, HabitationType, AdSearchRelation


# ModelForm
class AdModelForm(forms.ModelForm):
    moderation_comment = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Ad
        exclude = ('location', )


class SearchModelForm(forms.ModelForm):
    moderation_comment = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Search
        exclude = ('location', )


# ModelAdmin
class AdSearchRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'ad', 'search', 'ad_contacted', 'search_contacted', 'ad_notified', 'search_notified', 'valid']


class BaseAdmin(LeafletGeoAdmin):
    item_type = None

    def save_model(self, request, obj, form, change):
        # Override admin save_model
        # If obj.valid = True => accepted, send mail to user
        # If obj.valid = False => not accepted, send mail to user
        if obj.valid is True:
            # Send mail
            message = u'''Bonjour,
            \n\nVotre %s a été validée : %s .
            \n\nÀ bientôt
            \n\nL'équipe AcheterSansCom
            ''' % (self.item_type, obj.full_url)
            sender = "contact@acheternsanscom.com"
            recipients = [obj.user.email, ]
            subject = u"[AcheterSansCom] Votre %s a été validée - %s" % (self.item_type, obj)
        if obj.valid is False:
            # Send mail
            message = u'''Bonjour,
            \n\nVotre %s a été refusée : %s .
            \n\nRaison du refus : %s
            \n\nÀ bientôt
            \n\nL'équipe AcheterSansCom
            ''' % (self.item_type, obj.full_url, form.cleaned_data['moderation_comment'])
            sender = "contact@acheternsanscom.com"
            recipients = [obj.user.email, ]
            subject = u"[AcheterSansCom] Votre %s a été refusée - %s" % (self.item_type, obj)
        if obj.valid is not None:
            mail = EmailMessage(subject, message, sender, recipients, [sender])
            mail.send()
        obj.save(valid=obj.valid)


class AdAdmin(BaseAdmin):
    list_display = ['slug', 'price', 'surface', 'transaction']
    list_filter = ('transaction', 'valid')
    form = AdModelForm
    item_type = "annonce"


class SearchAdmin(BaseAdmin):
    list_display = ['slug', 'price_max', 'surface_min', 'location']
    list_filter = ('transaction', 'valid')
    form = SearchModelForm
    item_type = "recherche"


admin.site.register(Ad, AdAdmin)
admin.site.register(AdPicture)
admin.site.register(HabitationType)
admin.site.register(Search, SearchAdmin)
admin.site.register(AdSearchRelation, AdSearchRelationAdmin)
