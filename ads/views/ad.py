#-*- coding: utf-8 -*-
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, DeleteView, ListView

from ads.models import Ad, AdPicture, AdSearchRelation
from ads.forms import EditAdForm, EditAdFormWithLogin, ContactForm, SearchAdForm, AdPictureForm

from .utils import SetUserAndTransactionMixin, FillInitialForm, MessageDetailView, LoginRequiredMixin, AssureOwnerMixin


class AdPictureInline(InlineFormSet):
    """ Ad Picture InlineFormSet """
    model = AdPicture
    form = AdPictureForm
    extra = 4
    max_num = 4


class CreateAdView(SetUserAndTransactionMixin, FillInitialForm, CreateWithInlinesView):
    model = Ad
    form_class = EditAdForm
    transaction = None
    inlines = [AdPictureInline, ]

    def get_form_class(self):
        if self.request.user.is_anonymous():
            self.form_class = EditAdFormWithLogin
        else:
            self.form_class = EditAdForm
        return self.form_class

    def dispatch(self, request, *args, **kwargs):
        self.transaction = request.resolver_match.namespace
        return super(CreateAdView, self).dispatch(request, *args, **kwargs)


class ReadAdView(DetailView):
    model = Ad
    contact_form = ContactForm
    owner = False

    def get_context_data(self, **kwargs):
        context = super(ReadAdView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            if self.request.user == self.object.user:
                context['owner'] = True
            else:
                ars = AdSearchRelation.objects.filter(ad=self.object, search__user=self.request.user, valid=True)
                if ars.count() > 0:
                    if any(ars.values_list('ad_contacted', flat=True)):
                        context['already_contacted'] = True
                    context['contact_form'] = self.contact_form()
        return context


class AdDetailView(MessageDetailView):
    model = Ad
    detail_view = ReadAdView
    transaction = None


class UpdateAdView(LoginRequiredMixin, AssureOwnerMixin, UpdateWithInlinesView):
    model = Ad
    form_class = EditAdForm
    transaction = None
    inlines = [AdPictureInline, ]


class DeleteAdView(LoginRequiredMixin, AssureOwnerMixin, DeleteView):
    model = Ad
    transaction = None

    def get_success_url(self):
        slug = self.request.user.username
        return reverse_lazy('user_account', kwargs={'slug':slug, })


class AdListView(ListView):
    model = Ad
    paginate_by = 10

    transaction = None

    _valid = False
    _total = False
    _urlencode_get = ''


    def get(self, request, *args, **kwargs):
        get = super(AdListView, self).get(request, *args, **kwargs)
        if 'save_ad' in self.request.GET and self._valid:
            q = self.request.GET.urlencode()
            return HttpResponseRedirect(reverse('%s:ads_search_add' % self.transaction) + '?%s' % q)
        return get

    def get_queryset(self):
        q = super(AdListView, self).get_queryset().order_by('-modified')
        # Filter by transaction (sale or rent)
        q = q.filter(transaction=self.transaction)
        # here we remove the page from request.GET
        data = self.request.GET.copy()
        if 'page' in data:
            del data['page']
        self.form = SearchAdForm(data or None)
        if self.form.is_valid():
            price_max = self.form.cleaned_data['price_max']
            rooms_min = self.form.cleaned_data['rooms_min']
            surface_min = self.form.cleaned_data['surface_min']
            habitation_types = self.form.cleaned_data['habitation_types']
            location = self.form.cleaned_data['location']
            self._urlencode_get = data.urlencode()
            q = q.filter(price__lte=price_max)\
                 .filter(surface__gte=surface_min)\
                 .filter(habitation_type__in=habitation_types)\
                 .filter(location__within=location)
            if rooms_min:
                q = q.filter(rooms__gte=rooms_min)
            self._total = q.count()
            self._valid = True
        return q

    def get_context_data(self, **kwargs):
        context = super(AdListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['valid'] = self._valid
        context['total'] = self._total
        if self._urlencode_get != '':
            context['urlencode_get'] = '&%s' % self._urlencode_get
        return context

    def dispatch(self, request, *args, **kwargs):
        self.transaction = request.resolver_match.namespace
        return super(AdListView, self).dispatch(request, *args, **kwargs)
