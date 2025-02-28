from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from . import forms
from .forms import SelectCityHotelForm, UserUpdateForm, UserPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm


import requests
import json
import re

def hotel_booking(request):
    if request.method == 'POST':
        form = SelectCityHotelForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            checkin_date = form.cleaned_data['check_in_date']
            found_date = r'(\d{4}-\d{2}-\d{2})\s*—\s*(\d{4}-\d{2}-\d{2})'
            match = re.search(found_date, checkin_date)
            if match:
                checkIn = match.group(1)
                checkOut = match.group(2)
            
            
            adults_count = form.cleaned_data['adults_childs_count']
            found_count_adults_and_childs = re.findall(r"\d+", adults_count)
            found_count_adults_and_childs = list(map(int, found_count_adults_and_childs))
            adults = found_count_adults_and_childs[0]
            childs = found_count_adults_and_childs[1] if len(found_count_adults_and_childs) > 1 else 0

            # Запрос к API travelpayouts для поиска отелей
            api_url_city = f'https://engine.hotellook.com/api/v2/lookup.json?query={city}&lang=ru&lookFor=city&limit=1'
            api_request = requests.get(api_url_city)
            api_city_id = json.loads(api_request.text)
            print(api_city_id)
            city_id = api_city_id['results']['locations'][0]['id']
            
            
            #url = f'https://engine.hotellook.com/api/v2/cache.json?locationId={city_id}&checkIn={checkIn}&checkOut={checkOut}&adultsCount={adults}&childrenCount={childs}&currency=RUB&lang=ru&limit=20&waitForResult=0&token=3f700de13b6a11b3623be3a9477ff3f4'
            url = f'https://yasen.hotellook.com/tp/public/widget_location_dump.json?currency=rub&language=ru&limit=30&id={city_id}&type=popularity&check_in={checkIn}&check_out={checkOut}&adultsCount={adults}&childrenCount={childs}&token=3f700de13b6a11b3623be3a9477ff3f4'
            response = requests.get(url)
            hotels = json.loads(response.text)
            print(hotels)
            
            
            hotel_photos = []
            for hotel in hotels['popularity']:
                hotel_id = hotel['hotel_id']
                # Запрос на фотографии отелей
                photo_hotels = f'https://yasen.hotellook.com/photos/hotel_photos?id={hotel_id}'
                photo_hotels_request = requests.get(photo_hotels)
                photo_hotels_response = json.loads(photo_hotels_request.text)
                #print(photo_hotels_response)
                
                if photo_hotels_response.get(f'{hotel_id}'):
                    photo_id = photo_hotels_response[f'{hotel_id}']
                    hotel_photos.append(photo_id)
                else:  # Если нет фотографий, добавить placeholder (пустое место)
                    hotel_photos.append([])

           # print(hotel_photos)
            request.session['hotels'] = hotels
            request.session['hotel_photos'] = hotel_photos
            request.session['city'] = city
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SelectCityHotelForm()
    return render(request, 'index.html', {'form': form})


def search_hotels(request):
    hotels = request.session.get('hotels', [])
    hotel_photos = request.session.get('hotel_photos', [])
    city = request.session.get('city', [])
    
    #print(hotels)
    hotel_data = []
    for i, hotel in enumerate(hotels['popularity']):
        photo = hotel_photos[i]
        cover_photo = None
        if photo:
            cover_photo = f'https://photo.hotellook.com/image_v2/limit/{photo[0]}/800/520.auto'
        last_price_info = hotel.get('last_price_info')

        if last_price_info is not None:
            hotel_name = hotel['name']
            yandex_map =  f"https://yandex.ru/maps/?text={city}+{hotel_name}"
            hotel_data.append({
                'hotel_id': hotel['hotel_id'],
                'hotelName': hotel['name'],
                'priceAvg': int(last_price_info['price']),
                'stars': hotel['stars'],
                'distance': hotel['distance'],
                'property_type': hotel['property_type'],
                'nights': hotel['last_price_info']['nights'],
                'has_wifi': hotel['has_wifi'],
                'photo': cover_photo,
                'url': yandex_map,
            })
    #print(hotel_data)
    

    def get_star(hotel_data):
        stars = hotel_data.get('stars')
        if 1 <= stars <= 5:
            return '<img src="../static/svg_icon/star.svg">'.join([''] * stars)
        else:
            return str(stars)
    return render(request, 'search_results.html', {'hotels': hotel_data, 'get_star': get_star})


def hotel_detail(request, hotel_id):
    hotels = request.session.get('hotels', [])
    hotel_photos = request.session.get('hotel_photos', [])
    print(hotels)

    hotel = None
    photo = None
    for i, h in enumerate(hotels['popularity']):
        if h['hotel_id'] == hotel_id:
            hotel = h
            hotel['rating'] /= 10
            photos = hotel_photos[i]
            break
    
    print(hotel)
    photo_urls = [f'https://photo.hotellook.com/image_v2/limit/{photo_id}/800/520.jpg' for photo_id in photos]
        
    
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'photo_urls': photo_urls})


def registration(request):
    if request.method == 'POST':
        registr_form = forms.UserRegistrationForm(request.POST)
        if registr_form.is_valid():
            new_user = registr_form.save(commit=False)
            new_user.set_password(registr_form.cleaned_data['password'])
            new_user.save()
            
            username = registr_form.cleaned_data.get('username')
            password = registr_form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("hotel_reservations:home")
    else:
        registr_form = forms.UserRegistrationForm()
        
    return render(request, 'registration/registration.html', {'registr_form': registr_form})

def user_login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user_login = authenticate(username=username, password=password)
            if user_login is not None:
                login(request, user_login)
                return redirect('hotel_reservations:home')
    else:
        form = forms.UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})
  
@login_required        
def profile_user(request):
    update_user_form = UserUpdateForm(instance=request.user)
    password_form = UserPasswordChangeForm(request.user)
    
    if request.method == 'POST':
        type_form = request.POST.get('type_form')
        
        if type_form == 'update_user':
            update_user_form = UserUpdateForm(request.POST, instance=request.user)
            if update_user_form.is_valid():
                update_user_form.save()
                return redirect('hotel_reservations:profile')
        
        if type_form == 'change_password':
            password_form = UserPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('hotel_reservations:profile')
    else:
        update_user_form = UserUpdateForm(instance=request.user)
        password_form = UserPasswordChangeForm(request.user)


    return render(request, 'profile/user_profile.html', {'update_user_form': update_user_form, 'password_form': password_form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    form_class = CustomPasswordResetForm

class CustomUserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm


def user_logout(request):
    logout(request)
    return redirect('hotel_reservations:home')


def user_orders(request):
    return render(request, 'profile/user_orders.html')    

def policy_privacy(request):
    return render(request, 'policy_privacy.html')