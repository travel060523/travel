from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.urls import reverse

from django.contrib.auth import login as auth_login

import datetime

import time

import csv
import xlwt
from io import BytesIO

# Подключение моделей
from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models import Q

from .models import Country, Region, Hotel, ViewHotel, Claim, Reviews, News
# Подключение форм
from .forms import CountryForm, RegionForm, HotelForm, ClaimForm, ClaimFormEdit, ReviewsForm, NewsForm, SignUpForm

from django.contrib.auth.models import AnonymousUser

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница 
def index(request):
    news1 = News.objects.all().order_by('-daten')[0:1]
    news24 = News.objects.all().order_by('-daten')[1:4]
    country14 = Country.objects.all().order_by('?')[0:4]
    hotel14 = ViewHotel.objects.all().order_by('?')[0:4]
    reviews14 = Reviews.objects.all().order_by('?')[0:4]
    return render(request, "index.html", {"news1": news1, "news24": news24, "country14": country14, "hotel14": hotel14, "reviews14": reviews14, })    

# Контакты
def contact(request):
    return render(request, "contact.html")

# Кабинет
@login_required
def cabinet(request):
    claim = Claim.objects.filter(user_id=request.user.id).order_by('-datec')   
    reviews = Reviews.objects.filter(user_id=request.user.id).order_by('-dater')    
    return render(request, "cabinet.html", {"claim": claim, "reviews": reviews, })

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def country_index(request):
    try:
        country = Country.objects.all().order_by('title')
        return render(request, "country/index.html", {"country": country,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def country_create(request):
    try:
        if request.method == "POST":
            country = Country()
            country.title = request.POST.get("title")
            country.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                country.photo = request.FILES['photo']        
            countryform = CountryForm(request.POST)
            if countryform.is_valid():
                country.save()
                return HttpResponseRedirect(reverse('country_index'))
            else:
                return render(request, "country/create.html", {"form": countryform})
        else:        
            countryform = CountryForm()
            return render(request, "country/create.html", {"form": countryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def country_edit(request, id):
    try:
        country = Country.objects.get(id=id)
        if request.method == "POST":
            country.title = request.POST.get("title")
            country.details = request.POST.get("details")        
            if 'photo' in request.FILES:                
                country.photo = request.FILES['photo']        
            countryform = CountryForm(request.POST)
            if countryform.is_valid():
                country.save()
                return HttpResponseRedirect(reverse('country_index'))
            else:
                return render(request, "country/edit.html", {"form": countryform})
        else:
            # Загрузка начальных данных
            countryform = CountryForm(initial={'title': country.title, 'details': country.details, 'photo': country.photo, })
            return render(request, "country/edit.html", {"form": countryform})
    except Country.DoesNotExist:
        return HttpResponseNotFound("<h2>Country not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def country_delete(request, id):
    try:
        country = Country.objects.get(id=id)
        country.delete()
        return HttpResponseRedirect(reverse('country_index'))
    except Country.DoesNotExist:
        return HttpResponseNotFound("<h2>Country not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def country_read(request, id):
    try:
        country = Country.objects.get(id=id) 
        region = Region.objects.filter(country_id=id).order_by('title')
        if request.method == "POST":
            if 'searchBtn' in request.POST:
                reg = request.POST.get('radio_region')
                print(reg)
                hotel = ViewHotel.objects.filter(country_id=id).filter(region=reg).order_by('title')
                return render(request, "country/read.html", {"country": country, "region": region, "hotel": hotel, "reg": reg})
            else:
                # Выделить id отеля
                hotel_id = request.POST.dict().get("hotel_id")
                print("hotel_id ", hotel_id)
                price = request.POST.dict().get("price")
                print("price ", price)
                user = request.POST.dict().get("user")
                print("user ", user)
                # Перейти к созданию заявки
                return HttpResponseRedirect(reverse('claim_create', args=(hotel_id,)))
        else:
            hotel = ViewHotel.objects.filter(country_id=id).order_by('title')
            return render(request, "country/read.html", {"country": country, "region": region, "hotel": hotel})
    except Country.DoesNotExist:
        return HttpResponseNotFound("<h2>Country not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def region_index(request):
    try:
        region = Region.objects.all().order_by('title')
        return render(request, "region/index.html", {"region": region,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def region_create(request):
    try:
        if request.method == "POST":
            region = Region()
            region.country = Country.objects.filter(id=request.POST.get("country")).first()
            region.title = request.POST.get("title")
            regionform = RegionForm(request.POST)
            if regionform.is_valid():
                region.save()
                return HttpResponseRedirect(reverse('region_index'))
            else:
                return render(request, "region/create.html", {"form": regionform})
        else:        
            regionform = RegionForm()
            return render(request, "region/create.html", {"form": regionform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def region_edit(request, id):
    try:
        region = Region.objects.get(id=id)
        if request.method == "POST":
            region.country = Country.objects.filter(id=request.POST.get("country")).first()
            region.title = request.POST.get("title")
            regionform = RegionForm(request.POST)
            if regionform.is_valid():
                region.save()
                return HttpResponseRedirect(reverse('region_index'))
            else:
                return render(request, "region/edit.html", {"form": regionform})
        else:
            # Загрузка начальных данных
            regionform = RegionForm(initial={'country': region.country, 'title': region.title, })
            return render(request, "region/edit.html", {"form": regionform})
    except Region.DoesNotExist:
        return HttpResponseNotFound("<h2>Region not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def region_delete(request, id):
    try:
        region = Region.objects.get(id=id)
        region.delete()
        return HttpResponseRedirect(reverse('region_index'))
    except Region.DoesNotExist:
        return HttpResponseNotFound("<h2>Region not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def region_read(request, id):
    try:
        region = Region.objects.get(id=id) 
        return render(request, "region/read.html", {"region": region})
    except Region.DoesNotExist:
        return HttpResponseNotFound("<h2>Region not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def hotel_index(request):
    try:
        hotel = Hotel.objects.all().order_by('title')
        return render(request, "hotel/index.html", {"hotel": hotel,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def hotel_list(request):
    try:
        #hotel = Hotel.objects.all().order_by('title')
        hotel = ViewHotel.objects.all().order_by('title')
        #country = Country.objects.order_by('title').values_list('title', flat=True).distinct()
        #region = Region.objects.order_by('title').values_list('title', flat=True).distinct()
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                #item_country_title = request.POST.get('item_country_title')
                #print(item_country_title)
                #country_query = Country.objects.filter(title = item_country_title).only('id').all()
                #print(country_query)
                #region_query = Region.objects.filter(country_id__in = country_query).only('id').all()
                #print(region_query)                
                #hotel = Hotel.objects.filter(region_id__in=region_query).order_by('title')   
                #print(hotel)
                #return render(request, "hotel/list.html", {"hotel": hotel, "country": country, "item_country_title" : item_country_title,})
                # Список отелей
                #hotel = Hotel.objects.all()
                hotel = ViewHotel.objects.all()
                # Поиск по названию страны
                countrys_search = request.POST.get("countrys_search")
                #print(countrys_search)
                if countrys_search != '':
                    country_query = Country.objects.filter(title__contains = countrys_search).only('id').all()
                    #print(country_query)
                    region_query = Region.objects.filter(country_id__in = country_query).only('id').all()
                    #print(region_query)                
                    hotel = hotel.filter(region_id__in=region_query)
                # Поиск по названию региона
                regions_search = request.POST.get("regions_search")
                #print(regions_search)
                if regions_search != '':
                    region_query = Region.objects.filter(title__contains = regions_search).only('id').all()
                    #print(region_query)
                    hotel = hotel.filter(region_id__in=region_query)
                # Поиск по названию отеля
                hotels_search = request.POST.get("hotels_search")
                print(hotels_search)
                if hotels_search != '':
                    hotel = hotel.filter(title__contains = hotels_search).only('id').all()
                    print(hotel)
                    hotel = hotel.filter(region_id__in=region_query)
                # Сортировка
                hotel = hotel.order_by('title')
                return render(request, "hotel/list.html", {"hotel": hotel, "countrys_search" : countrys_search, "regions_search" : regions_search, "hotels_search" : hotels_search,})
            elif 'resetBtn' in request.POST:            
                #hotel = Hotel.objects.all().order_by('title')
                hotel = ViewHotel.objects.all().order_by('title')
                return render(request, "hotel/list.html", {"hotel": hotel, })
            else:
                # Выделить id отеля
                hotel_id = request.POST.dict().get("hotel_id")
                print("hotel_id ", hotel_id)
                price = request.POST.dict().get("price")
                print("price ", price)
                user = request.POST.dict().get("user")
                print("user ", user)
                # Перейти к созданию заявки
                return HttpResponseRedirect(reverse('claim_create', args=(hotel_id,)))            
        else:
            #return render(request, "hotel/list.html", {"hotel": hotel, "country": country, "region": region, })
            return render(request, "hotel/list.html", {"hotel": hotel, })
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def hotel_create(request):
    try:
        if request.method == "POST":
            hotel = Hotel()
            hotel.region = Region.objects.filter(id=request.POST.get("region")).first()
            hotel.title = request.POST.get("title")
            hotel.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                hotel.photo = request.FILES['photo']        
            hotel.price = request.POST.get("price")
            hotelform = HotelForm(request.POST)
            if hotelform.is_valid():
                hotel.save()
                return HttpResponseRedirect(reverse('hotel_index'))
            else:
                return render(request, "hotel/create.html", {"form": hotelform})
        else:        
            hotelform = HotelForm()
            return render(request, "hotel/create.html", {"form": hotelform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def hotel_edit(request, id):
    try:
        hotel = Hotel.objects.get(id=id)
        if request.method == "POST":
            hotel.region = Region.objects.filter(id=request.POST.get("region")).first()
            hotel.title = request.POST.get("title")
            hotel.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                hotel.photo = request.FILES['photo']        
            hotel.price = request.POST.get("price")
            hotelform = HotelForm(request.POST)
            if hotelform.is_valid():
                hotel.save()
                return HttpResponseRedirect(reverse('hotel_index'))
            else:
                return render(request, "hotel/edit.html", {"form": hotelform})
        else:
            # Загрузка начальных данных
            hotelform = HotelForm(initial={'region': hotel.region, 'title': hotel.title, 'details': hotel.details, 'photo': hotel.photo, 'price': hotel.price, })
            return render(request, "hotel/edit.html", {"form": hotelform})
    except Hotel.DoesNotExist:
        return HttpResponseNotFound("<h2>Hotel not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def hotel_delete(request, id):
    try:
        hotel = Hotel.objects.get(id=id)
        hotel.delete()
        return HttpResponseRedirect(reverse('hotel_index'))
    except Hotel.DoesNotExist:
        return HttpResponseNotFound("<h2>Hotel not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def hotel_read(request, id):
    try:
        #hotel = Hotel.objects.get(id=id) 
        hotel = ViewHotel.objects.get(id=id) 
        # Отзывы на данный отель
        reviews = Reviews.objects.filter(hotel_id=id).exclude(rating=None)
        return render(request, "hotel/read.html", {"hotel": hotel, "reviews": reviews})
    except Hotel.DoesNotExist:
        return HttpResponseNotFound("<h2>Hotel not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def claim_index(request):
    try:
        claim = Claim.objects.all().order_by('-datec')
        return render(request, "claim/index.html", {"claim": claim,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
#@group_required("Managers")
def claim_create(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)
        print(hotel)
        if request.method == "POST":
            claim = Claim()
            claim.user = request.user
            #claim.hotel = Hotel.objects.filter(id=request.POST.get("hotel")).first()
            claim.hotel_id = hotel_id
            claim.start = request.POST.get("start")
            claim.finish = request.POST.get("finish")
            claim.details = request.POST.get("details") + ". \r\n" + _('room') + ": " + request.POST.get("room")
            claim.user_id = request.user.id
            claimform = ClaimForm(request.POST)
            if claimform.is_valid():
                claim.save()
                return HttpResponseRedirect(reverse('cabinet'))
            else:
                return render(request, "claim/create.html", {"form": claimform, "hotel": hotel, })
        else:        
            claimform = ClaimForm(initial={'start': (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d'), 'finish': (datetime.datetime.now() + datetime.timedelta(days=37)).strftime('%Y-%m-%d'), })
            return render(request, "claim/create.html", {"form": claimform, "hotel": hotel, })
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def claim_edit(request, id):
    try:
        claim = Claim.objects.get(id=id)
        if request.method == "POST":
            #claim.hotel = Hotel.objects.filter(id=request.POST.get("hotel")).first()
            #claim.start = request.POST.get("start")
            #claim.finish = request.POST.get("finish")
            #claim.details = request.POST.get("details")
            claim.result = request.POST.get("result")
            claimform = ClaimFormEdit(request.POST)
            if claimform.is_valid():
                claim.save()
                return HttpResponseRedirect(reverse('claim_index'))
            else:
                return render(request, "claim/edit.html", {"form": claimform, "claim": claim, })
        else:
            # Загрузка начальных данных
            claimform = ClaimFormEdit(initial={'result': claim.result, })
            return render(request, "claim/edit.html", {"form": claimform, "claim": claim, })
    except Claim.DoesNotExist:
        return HttpResponseNotFound("<h2>Claim not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def claim_delete(request, id):
    try:
        claim = Claim.objects.get(id=id)
        claim.delete()
        return HttpResponseRedirect(reverse('claim_index'))
    except Claim.DoesNotExist:
        return HttpResponseNotFound("<h2>Claim not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def claim_read(request, id):
    try:
        claim = Claim.objects.get(id=id) 
        return render(request, "claim/read.html", {"claim": claim})
    except Claim.DoesNotExist:
        return HttpResponseNotFound("<h2>Claim not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для просмотра
def reviews_list(request):
    reviews = Reviews.objects.all().order_by('-dater')
    return render(request, "reviews/list.html", {"reviews": reviews})

# Список для просмотра с кнопкой удалить
@login_required
@group_required("Managers")
def reviews_index(request):
    reviews = Reviews.objects.all().order_by('-dater')
    return render(request, "reviews/index.html", {"reviews": reviews})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
def reviews_create(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    if request.method == "POST":
        reviews = Reviews()        
        #reviews.hotel = Hotel.objects.filter(id=request.POST.get("hotel")).first()
        reviews.hotel_id = hotel_id
        reviews.rating = request.POST.get("rating")
        reviews.details = request.POST.get("details")
        reviews.user = request.user
        reviewsform = ReviewsForm(request.POST)
        if reviewsform.is_valid():
            reviews.save()
            return HttpResponseRedirect(reverse('cabinet'))
        else:
            return render(request, "reviews/create.html", {"form": reviewsform,  "hotel": hotel, })     
    else:        
        reviewsform = ReviewsForm(initial={'rating': 5, })
        return render(request, "reviews/create.html", {"form": reviewsform, "hotel": hotel, })

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def reviews_delete(request, id):
    try:
        reviews = Reviews.objects.get(id=id)
        reviews.delete()
        return HttpResponseRedirect(reverse('reviews_index'))
    except Reviews.DoesNotExist:
        return HttpResponseNotFound("<h2>Reviews not found</h2>")


###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        #news = News.objects.all().order_by('surname', 'name', 'patronymic')
        #return render(request, "news/index.html", {"news": news})
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/list.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']        
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:        
            #newsform = NewsForm(request.FILES, initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'),})
            newsform = NewsForm(initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return HttpResponseRedirect(reverse('index'))
                #return render(request, 'registration/register_done.html', {'new_user': user})
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    try:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        template_name = 'registration/my_account.html'
        success_url = reverse_lazy('index')
        #success_url = reverse_lazy('my_account')
        def get_object(self):
            return self.request.user
    except Exception as exception:
        print(exception)



