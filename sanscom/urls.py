from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls.static import static
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sanscom.views.home', name='home'),
    url(r'^$', RedirectView.as_view(pattern_name='sale:ads_ad_list')),
    #url(r'^', include('ads.urls')),
    url(r'^vente/', include('ads.urls', namespace='sale', app_name='ads')),
    url(r'^location/', include('ads.urls', namespace='rent', app_name='ads')),
    url(r'^admin/', include(admin.site.urls)),
    #(r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/', include('accounts.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^a-propos/$', 'flatpage', {'url': '/a-propos/'}, name='a-propos'),
    url(r'^legal/$', 'flatpage', {'url': '/legal/'}, name='legal'),
    url(r'^cgu/$', 'flatpage', {'url': '/cgu/'}, name='cgu'),
)
