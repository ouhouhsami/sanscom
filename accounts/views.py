from django.views.generic import DetailView, UpdateView
from django.shortcuts import redirect

from ads.models import Ad, Search
from ads.views import AssureOwnerMixin

from .models import UserProfile
from .forms import EditUserAccountForm


class UserAccount(DetailView):
    slug_field = 'user__username'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super(UserAccount, self).get_context_data(**kwargs)
        ad_manager = Ad.valid_objects
        search_manager = Search.valid_objects
        user_profile = self.get_object()
        if user_profile.user == self.request.user:
            context['owner'] = True
            ad_manager = Ad.objects
            search_manager = Search.objects
        # Fill appropriate context variables
        context['ads'] = ad_manager.filter(user=user_profile.user)
        context['rentals'] = ad_manager.filter(user=user_profile.user, transaction="rent")
        context['sales'] = ad_manager.filter(user=user_profile.user, transaction="sale")
        context['rent_searches'] = search_manager.filter(user=user_profile.user, transaction="rent")
        context['sale_searches'] = search_manager.filter(user=user_profile.user, transaction="sale")
        return context


class UpdateUserAccount(AssureOwnerMixin, UpdateView):
    slug_field = 'user__username'
    form_class = EditUserAccountForm
    model = UserProfile


def redirect_profile(request):
    user = request.user
    return redirect('user_account', slug=user.username)
