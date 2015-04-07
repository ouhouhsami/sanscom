#-*- coding: utf-8 -*-
import requests

from django import forms

from django.contrib.gis import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate

from .utils import geo_from_address, WrongAddressError
from .models import Ad, Search, HabitationType, AdPicture
from .widgets import ExtendedLeafletWidget

from floppyforms.widgets import RadioSelect as FloppyRadioSelect


class NullBooleanRadioSelect(FloppyRadioSelect):
    template_name = "widgets/radio.html"
    def __init__(self, *args, **kwargs):
        choices = (
            (None, _('Indifférent')),
            (True, _('Oui')),
            (False, _('Non'))
        )
        super(NullBooleanRadioSelect, self).__init__(choices=choices, *args, **kwargs)

    _empty_value = None


class BooleanRadioSelect(FloppyRadioSelect):
    template_name = "widgets/booleanradio.html"


class AdPictureForm(forms.ModelForm):

    class Meta:
        model = AdPicture
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Description de la photo', }),
            'image': forms.FileInput
        }
        fields = '__all__'


class WithLogin(forms.ModelForm):
    # clean if username and password
    # or 3
    def clean(self):
        cleaned_data = super(WithLogin, self).clean()
        username = cleaned_data['username']
        email = cleaned_data['email']
        password = cleaned_data['password']
        password2 = cleaned_data['password2']
        login_username = cleaned_data['login_username']
        login_password = cleaned_data['login_password']

        login = cleaned_data['login']

        if login:
            # we are in login process
            a = authenticate(username=login_username, password=login_password)
            if not a:
                raise forms.ValidationError("Votre Nom d'utilisateur et/ou votre Mot de passe ne sont pas valides.")
                self.add_error('login_username', "skksskskk")
        else:
            # we are in signup process
            if password != password2:
                raise forms.ValidationError("Les mots de passe sont différents.")
            existing = User.objects.filter(username__iexact=username)
            if existing.exists():
                raise forms.ValidationError(_("A user with that username already exists."))

        return cleaned_data

    login = forms.BooleanField(required=False)  # keep state of user choice: signup or login

    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={}), required=False)
    email = forms.EmailField(label=_("Email"), widget=forms.TextInput(attrs={}), max_length=254, required=False)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput({}), required=False)
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput({}), required=False)

    login_username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={}), required=False)
    login_password = forms.CharField(label=_("Password"), widget=forms.PasswordInput({}), required=False)


class EditSearchForm(forms.ModelForm):
    habitation_types = forms.ModelMultipleChoiceField(queryset=HabitationType.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={}))

    def clean_location(self):
        location = self.cleaned_data['location']
        if location.area > 0.306579934754:
            raise forms.ValidationError("Entrer une zone de recherche plus petite")
        return location

    class Meta:
        model = Search
        exclude = ('user', 'transaction')
        widgets = {
            'location': ExtendedLeafletWidget(),
            'price_max': forms.TextInput(),
            'surface_min': forms.TextInput(),
            'ground_surface_min': forms.TextInput(),
            'description': forms.Textarea({'placeholder': 'Autres informations utiles aux vendeurs qui souhaiteraient vous contacter.', }),
            'ground_floor': NullBooleanRadioSelect,
            'top_floor': NullBooleanRadioSelect,
            'not_overlooked': NullBooleanRadioSelect,
            'elevator': NullBooleanRadioSelect,
            'intercom': NullBooleanRadioSelect,
            'digicode': NullBooleanRadioSelect,
            'doorman': NullBooleanRadioSelect,
            'kitchen': NullBooleanRadioSelect,
            'duplex': NullBooleanRadioSelect,
            'swimming_pool': NullBooleanRadioSelect,
            'alarm': NullBooleanRadioSelect,
            'air_conditioning': NullBooleanRadioSelect,
            'fireplace': NullBooleanRadioSelect,
            'terrace': NullBooleanRadioSelect,
            'balcony': NullBooleanRadioSelect,
            'separate_dining_room': NullBooleanRadioSelect,
            'separate_toilet': NullBooleanRadioSelect,
            'bathroom': NullBooleanRadioSelect,
            'shower': NullBooleanRadioSelect,
            'separate_entrance': NullBooleanRadioSelect,
            'cellar': NullBooleanRadioSelect,
            'parking':NullBooleanRadioSelect,
        }


class EditSearchFormWithLogin(WithLogin, EditSearchForm):

    def clean(self):
        cleaned_data = super(EditSearchFormWithLogin, self).clean()
        return cleaned_data

    class Meta(EditSearchForm.Meta):
        widgets = EditSearchForm.Meta.widgets


class SearchSearchForm(forms.ModelForm):

    #habitation_type = forms.ModelChoiceField(queryset=HabitationType.objects.all(), empty_label=None, widget=forms.RadioSelect(attrs={}))
    habitation_type = forms.ModelChoiceField(queryset=HabitationType.objects.all(), empty_label=None, widget=BooleanRadioSelect)

    def clean_address(self):
        address = self.cleaned_data['address']
        try:
            geo_from_address(address)
        except WrongAddressError:
            raise forms.ValidationError("Entrer une adresse valide")
        return address

    class Meta:
        model = Ad
        fields = ('address', 'price', 'surface', 'habitation_type', )
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Adresse', }),
            'price': forms.TextInput(attrs={'placeholder': 'Prix', }),
            'surface': forms.TextInput(attrs={'placeholder': 'Surface', }),
        }


class EditAdForm(forms.ModelForm):

    habitation_type = forms.ModelChoiceField(label="Type de bien", queryset=HabitationType.objects.all(), empty_label=None, widget=forms.RadioSelect(attrs={}))

    def clean_address(self):
        address = self.cleaned_data['address']
        url = "http://services.gisgraphy.com//geocoding/geocode?address='%s'&country=FR&format=json" % address
        r = requests.get(url)
        try:
            json = r.json()
            lat = json['result'][0]['lat']
            lng = json['result'][0]['lng']
            pt = "POINT(%s %s)" % (lng, lat)
        except:
            raise forms.ValidationError("Entrer une adresse valide")
        return address

    class Meta:
        model = Ad
        exclude = ('user', 'location', 'transaction', 'json_address')
        widgets = {
            'address': forms.TextInput(),
            'price': forms.TextInput(),
            'surface': forms.TextInput(),
            'surface_carrez': forms.TextInput(),
            'rooms': forms.TextInput(),
            'bedrooms': forms.TextInput(),
            'energy_consumption': forms.Select(),
            'ad_valorem_tax': forms.TextInput(),
            'housing_tax': forms.TextInput(),
            'maintenance_charges': forms.TextInput(),
            'emission_of_greenhouse_gases': forms.Select(),
            'ground_surface': forms.TextInput(),
            'floor': forms.TextInput(),
            'ground_floor': forms.CheckboxInput(),
            'top_floor': forms.CheckboxInput(),
            'not_overlooked': forms.CheckboxInput(),
            'elevator': forms.CheckboxInput(),
            'intercom': forms.CheckboxInput(),
            'digicode': forms.CheckboxInput(),
            'doorman': forms.CheckboxInput(),
            'heating': forms.Select(),
            'kitchen': forms.CheckboxInput(),
            'duplex': forms.CheckboxInput(),
            'swimming_pool': forms.CheckboxInput(),
            'alarm': forms.CheckboxInput(),
            'air_conditioning': forms.CheckboxInput(),
            'fireplace': forms.Select(),
            'terrace': forms.TextInput(),
            'balcony': forms.TextInput(),
            'separate_dining_room': forms.CheckboxInput(),
            'separate_toilet': forms.TextInput(),
            'bathroom': forms.TextInput(),
            'shower': forms.TextInput(),
            'separate_entrance': forms.CheckboxInput(),
            'cellar': forms.CheckboxInput(),
            'parking': forms.Select(),
            'orientation': forms.TextInput(),
            'description': forms.Textarea({'placeholder': 'Compléments d\'information', })
        }


class EditAdFormWithLogin(WithLogin, EditAdForm):
    pass


class SearchAdForm(forms.ModelForm):

    def clean_location(self):
        location = self.cleaned_data['location']
        if location.area > 0.306579934754:
            raise forms.ValidationError("Entrer une zone de recherche plus petite")
        return location

    class Meta:
        model = Search
        fields = ('location', 'price_max', 'surface_min', 'habitation_types', 'rooms_min')
        widgets = {
            'location': ExtendedLeafletWidget(),
            'price_max': forms.TextInput(),
            'surface_min': forms.TextInput(),
            'habitation_types': forms.CheckboxSelectMultiple()
        }


class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

