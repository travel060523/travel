"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static

from kaz import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('i18n/', include('django.conf.urls.i18n')),
    #path('export/excel/', views.export_excel, name='export_excel'),     

    path('cabinet/', views.cabinet, name='cabinet'),

    path('country/index/', views.country_index, name='country_index'),
    path('country/create/', views.country_create, name='country_create'),
    path('country/edit/<int:id>/', views.country_edit, name='country_edit'),
    path('country/delete/<int:id>/', views.country_delete, name='country_delete'),
    path('country/read/<int:id>/', views.country_read, name='country_read'),

    path('region/index/', views.region_index, name='region_index'),
    path('region/create/', views.region_create, name='region_create'),
    path('region/edit/<int:id>/', views.region_edit, name='region_edit'),
    path('region/delete/<int:id>/', views.region_delete, name='region_delete'),
    path('region/read/<int:id>/', views.region_read, name='region_read'),

    path('hotel/index/', views.hotel_index, name='hotel_index'),
    path('hotel/list/', views.hotel_list, name='hotel_list'),
    path('hotel/create/', views.hotel_create, name='hotel_create'),
    path('hotel/edit/<int:id>/', views.hotel_edit, name='hotel_edit'),
    path('hotel/delete/<int:id>/', views.hotel_delete, name='hotel_delete'),
    path('hotel/read/<int:id>/', views.hotel_read, name='hotel_read'),

    path('claim/index/', views.claim_index, name='claim_index'),
    path('claim/create/<int:hotel_id>/', views.claim_create, name='claim_create'),
    path('claim/edit/<int:id>/', views.claim_edit, name='claim_edit'),
    path('claim/delete/<int:id>/', views.claim_delete, name='claim_delete'),
    path('claim/read/<int:id>/', views.claim_read, name='claim_read'),

    path('reviews/index/', views.reviews_index, name='reviews_index'),
    path('reviews/list/', views.reviews_list, name='reviews_list'),
    path('reviews/create/<int:hotel_id>/', views.reviews_create, name='reviews_create'),
    path('reviews/delete/<int:id>/', views.reviews_delete, name='reviews_delete'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

