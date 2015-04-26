from leaflet.admin import LeafletGeoAdmin

from django.contrib import admin
from .models import Ad, AdPicture, Search, HabitationType, AdSearchRelation


class AdSearchRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'ad', 'search', 'ad_contacted', 'search_contacted', 'ad_notified', 'search_notified', 'valid']


class AdAdmin(LeafletGeoAdmin):
    list_display = ['slug', 'price', 'surface', 'transaction']
    list_filter = ('transaction', )

    def save_model(self, request, obj, form, change):
        # Override admin save_model
        # If obj.valid = True => accepted, send mail to user
        # If obj.valid = False => not accepted, send mail to user
        obj.save(valid=obj.valid)


class SearchAdmin(LeafletGeoAdmin):
    list_display = ['slug', 'price_max', 'surface_min', 'location']

    def save_model(self, request, obj, form, change):
        # Override admin save_model
        # If obj.valid = True => accepted, send mail to user
        # If obj.valid = False => not accepted, send mail to user
        obj.save(valid=obj.valid)


admin.site.register(Ad, AdAdmin)
admin.site.register(AdPicture)
admin.site.register(HabitationType)
admin.site.register(Search, SearchAdmin)
admin.site.register(AdSearchRelation, AdSearchRelationAdmin)
