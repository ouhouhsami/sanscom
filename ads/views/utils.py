#-*- coding: utf-8 -*-
from sortable_listview import SortableListView

from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from accounts.models import UserProfile

from ads.models import Ad, Search, AdSearchRelation
from ads.forms import ContactForm


# Mixins
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class SetUserAndTransactionMixin(object):
    """
    Both form_valid and forms_valid are required, to deal with
    CreateWithInlinesView and UpdateWithInlinesView implementation.
    """

    def get_or_create_and_login_user(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        login_username = form.cleaned_data['login_username']
        login_password = form.cleaned_data['login_password']
        _login = form.cleaned_data['login']
        if login_username:
            user = authenticate(username=login_username, password=login_password)
        else:
            user = User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            UserProfile(user=user).save()
        login(self.request, user)

    def forms_valid(self, form, inlines):
        if self.request.user.is_anonymous():
            self.get_or_create_and_login_user(form)
        form.instance.user = self.request.user
        form.instance.transaction = self.transaction
        return super(SetUserAndTransactionMixin, self).forms_valid(form, inlines)

    def form_valid(self, form):
        if self.request.user.is_anonymous():
            self.get_or_create_and_login_user(form)
        form.instance.user = self.request.user
        form.instance.transaction = self.transaction
        return super(SetUserAndTransactionMixin, self).form_valid(form)


class AssureOwnerMixin(object):
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = self.model.objects.get(**{self.slug_field: self.kwargs['slug']})
        if not obj.user == self.request.user:
            raise Http404
        return obj


class FillInitialForm(object):
    def get_initial(self):
        initial = super(FillInitialForm, self).get_context_data()
        if self.request.GET:
            form = self.form_class(self.request.GET)
            return form.data.dict()
        return initial

# Utils
class MessageView(SingleObjectMixin, FormView):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        self.request = request
        return super(MessageView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # I think we don't need this test here!
        if form.is_valid():
            # TODO: need to test if we can send this mail !
            # if user is autorized to = if ad/search fit together
            message = form.cleaned_data['message']
            sender = self.request.user.email
            recipients = [self.get_object().user.email, ]
            subject = "[AcheterSansCom] Message à propos de %s" % self.get_object()
            mail = EmailMessage(subject, message, sender, recipients, [sender])
            mail.send()
            # We send a copy of the mail to the sender
            sender_subject = "[AcheterSansCom] Message envoyé à propos de %s " % self.get_object()
            sender_message = u"Bonjour, \nVoici le message que vous avez envoyé : \n %s" % (message)
            sender_mail = EmailMessage(sender_subject, sender_message, "contact@achetersanscom.com", [self.request.user.email, ], ["contact@achetersanscom.com"])
            sender_mail.send()
            # here we must set 'contacted'
            # UGLY ...
            if self.model == Search:
                asr = AdSearchRelation.objects.filter(search=self.object, ad__user=self.request.user)
                asr.update(search_contacted=timezone.now())
            else:
                asr = AdSearchRelation.objects.filter(ad=self.object, search__user=self.request.user)
                asr.update(ad_contacted=timezone.now())
        return super(MessageView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(contact_form=form))

    def get_template_names(self):
        if self.model == Ad:
            return "ads/ad_detail.html"
        if self.model == Search:
            return "ads/search_detail.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class MessageDetailView(DetailView):
    model = Ad
    contact_form = ContactForm
    detail_view = None

    def get(self, request, *args, **kwargs):
        view = self.detail_view.as_view(model=self.model, contact_form=self.contact_form, template_name=self.template_name)
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MessageView.as_view(model=self.model, form_class=self.contact_form)
        return view(request, *args, **kwargs)


class CustomSortableListView(SortableListView):
    '''
    This is ugly
    '''
    def get_querystring(self):
        """
        Clean existing query string (GET parameters) by removing
        arguments that we don't want to preserve (sort parameter, 'page')
        """
        to_remove = self.get_querystring_parameter_to_remove()
        query_dict = self.request.GET.copy()
        for arg in to_remove:
            if arg in query_dict:
                query_dict.pop(arg)
        return query_dict.urlencode()

    def get_sort_link_list(self, request):
        sort_links = []
        for sort_field in self.allowed_sort_fields:
            sort_link_asc = {
                'attrs': sort_field,
                'path': self.get_basic_sort_link(request, sort_field, ''),
                'indicator': 'true' if self.get_sort_indicator(sort_field) == 'sort-asc' else '',
                'title': self.allowed_sort_fields[sort_field]['verbose_name_asc']}
            sort_link_dsc = {
                'attrs': sort_field,
                'path': self.get_basic_sort_link(request, sort_field, '-'),
                'indicator': 'true' if self.get_sort_indicator(sort_field) == 'sort-desc' else '',
                'title': self.allowed_sort_fields[sort_field]['verbose_name_dsc']}
            sort_links.append(sort_link_asc)
            sort_links.append(sort_link_dsc)
        return sort_links

    def get_context_data(self, **kwargs):
        context = super(CustomSortableListView, self).get_context_data(**kwargs)
        if self.sort_order:
            context['current_sort_label'] = self.allowed_sort_fields[self.sort_field]['verbose_name_dsc']
        else:
            context['current_sort_label'] = self.allowed_sort_fields[self.sort_field]['verbose_name_asc']
        return context

    def get_basic_sort_link(self, request, field, direction):
        """
        Thanks to del_query_parameters and get_querystring, we build the link
        with preserving interesting get parameters and removing the others
        """
        query_string = self.get_querystring()
        sort_string = "sort=" + direction + field
        sort_link = request.path + '?' + sort_string
        if query_string:
            sort_link += '&' + query_string
        return sort_link
