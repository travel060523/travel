from datetime import datetime
from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput, NumberInput, CheckboxInput
from .models import Country, Region, Hotel, Claim, Reviews, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import datetime
from django.utils import timezone

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['title', 'details', 'photo']
        widgets = {
            'title': TextInput(attrs={"size":"100"}),  
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),    
        }
    ## Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['country', 'title',]
        widgets = {
            'country': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'country': _('country_title'),            
        }
    ## Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['region', 'title', 'details', 'photo', 'price', ]
        widgets = {
            'region': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),   
            'price': NumberInput(attrs={"size":"10"}),
        }
        labels = {
            'region': _('region_title'),            
        }
    ## Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        #fields = ('hotel', 'start', 'finish', 'details')
        fields = ('start', 'finish', 'details')
        widgets = {
            #'hotel': forms.Select(attrs={'class': 'chosen'}),            
            'start': DateInput(format='%d/%m/%Y'),
            'finish': DateInput(format='%d/%m/%Y'),
            'start': TextInput(attrs={"type":"date"}),
            'finish': TextInput(attrs={"type":"date"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
        labels = {
            'hotel': _('hotel'),            
        }

class ClaimFormEdit(forms.ModelForm):
    class Meta:
        model = Claim
        #fields = ('hotel', 'start', 'finish', 'details')
        fields = ('result',)
        widgets = {
            #'user': forms.Select(attrs={'class': 'chosen', 'disabled': 'true'}),            
            #'hotel': forms.Select(attrs={'class': 'chosen', 'disabled': 'true'}),   
            #'start': DateTimeInput(format='%d/%m/%Y'),
            #'finish': DateTimeInput(format='%d/%m/%Y'),         
            #'details': Textarea(attrs={'cols': 100, 'rows': 10, 'readonly': 'readonly'}),           
            'result': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
        #labels = {
        #    'hotel': _('hotel'),            
        #}

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        #fields = ('hotel', 'details', 'rating')
        fields = ('details', 'rating')
        widgets = {
            #'hotel': forms.Select(attrs={'class': 'chosen'}),            
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
            'rating': forms.NumberInput(attrs={'max': '5', 'min': '1'}),            
        }
        #labels = {
        #    'hotel': _('hotel'),            
        #}


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'dater': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')