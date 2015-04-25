#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (CreateView, UpdateView,
                                  DeleteView)

from ads.models import Search, AdSearchRelation
from ads.forms import EditSearchForm, EditSearchFormWithLogin, ContactForm, SearchSearchForm
from ads.utils import geo_from_address

from .utils import SetUserAndTransactionMixin, FillInitialForm, MessageDetailView, LoginRequiredMixin, AssureOwnerMixin, CustomSortableListView, ModeratedDetailView


class CreateSearchView(SetUserAndTransactionMixin, FillInitialForm, CreateView):
    model = Search
    transaction = None

    def get_form_class(self):
        if self.request.user.is_anonymous():
            self.form_class = EditSearchFormWithLogin
        else:
            self.form_class = EditSearchForm
        return self.form_class

    def dispatch(self, request, *args, **kwargs):
        self.transaction = request.resolver_match.namespace
        return super(CreateSearchView, self).dispatch(request, *args, **kwargs)


class ReadSearchView(ModeratedDetailView):
    model = Search
    contact_form = ContactForm

    def get_context_data(self, **kwargs):
        # here we test if logged user can contact search owner
        context = super(ReadSearchView, self).get_context_data(**kwargs)
        context['contact_form'] = self.contact_form(self.request.user.is_authenticated())
        if self.request.user.is_authenticated():
            if self.request.user == self.object.user:
                context['owner'] = True
            else:
                ars = AdSearchRelation.objects.filter(search=self.object, ad__user=self.request.user, valid=True)
                if ars.count() > 0:
                    # if multiple offers from same vendor feet same search
                    # the vendor can only contact searcher one time
                    # this is what the line below does
                    if any(ars.values_list('search_contacted', flat=True)):
                        context['already_contacted'] = True
                    #context['contact_form'] = self.contact_form()
        return context


class SearchListView(CustomSortableListView):
    # model = Search
    queryset = Search.valid_objects
    paginate_by = 10
    transaction = None

    allowed_sort_fields = {
        'modified': {
            'default_direction': '-',
            'verbose_name': 'Date de mise en ligne',
            'verbose_name_asc': u'Plus anciennes',
            'verbose_name_dsc': u'Plus récentes',
            'order': 3},
        'price_max': {
            'default_direction': '',
            'verbose_name': 'Prix',
            'verbose_name_asc': u'Moins chères',
            'verbose_name_dsc': u'Plus chères'
        },
        'surface_min': {
            'default_direction': '',
            'verbose_name': 'Surface',
            'verbose_name_asc': u'Plus petites',
            'verbose_name_dsc': u'Plus grandes'
        },
    }

    default_sort_field = 'modified'

    _valid = False
    _urlencode_get = ''

    def get(self, request, *args, **kwargs):
        get = super(SearchListView, self).get(request, *args, **kwargs)
        if 'save_ad' in self.request.GET and self._valid:
            q = self.request.GET.urlencode()
            return HttpResponseRedirect(reverse('%s:ads_ad_add' % self.transaction) + '?%s' % q)
        return get

    def get_queryset(self):
        q = super(SearchListView, self).get_queryset()
        q = q.filter(transaction=self.transaction)
        data = self.request.GET.copy()
        if 'page' in data:
            del data['page']
        self.form = SearchSearchForm(data or None)
        if self.form.is_valid():
            price = self.form.cleaned_data['price']
            surface = self.form.cleaned_data['surface']
            habitation_type = self.form.cleaned_data['habitation_type']
            address = self.form.cleaned_data['address']
            location = geo_from_address(address)
            self._urlencode_get = data.urlencode()
            q = q.filter(price_max__gte=price)\
                 .filter(surface_min__lte=surface)\
                 .filter(habitation_types=habitation_type)\
                 .filter(location__contains=location)
            self._valid = True
        return q

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['valid'] = self._valid
        if self._urlencode_get != '':
            context['urlencode_get'] = '&%s' % self._urlencode_get
        return context

    def dispatch(self, request, *args, **kwargs):
        self.transaction = request.resolver_match.namespace
        return super(SearchListView, self).dispatch(request, *args, **kwargs)


class SearchDetailView(MessageDetailView):
    model = Search
    detail_view = ReadSearchView
    transaction = None


class UpdateSearchView(LoginRequiredMixin, AssureOwnerMixin, UpdateView):
    model = Search
    form_class = EditSearchForm
    transaction = None


class DeleteSearchView(LoginRequiredMixin, AssureOwnerMixin, DeleteView):
    model = Search
    transaction = None

    def get_success_url(self):
        slug = self.request.user.username
        return reverse_lazy('user_account', kwargs={'slug':slug, })
