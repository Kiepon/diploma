import json
import re
from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import SelectCityHotelForm
import requests


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
            url = f'https://engine.hotellook.com/api/v2/cache.json?location={city}&checkIn={checkIn}&checkOut={checkOut}&adultsCount={adults}&childrenCount={childs}&currency=RUB&limit=50'
            response = requests.get(url)
            hotels = json.loads(response.text)
            print(hotels)

            
            return render(request, 'search_results.html', {'form': form, 'hotels': hotels})
    else:
        form = SelectCityHotelForm()
    return render(request, 'index.html', {'form': form})


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
            return render(request, 'index.html', {'new_user': new_user})
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
                return redirect('home')
    else:
        form = forms.UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})
                # Return an 'invalid login' error message.
        
        
def user_logout(request):
    logout(request)
    return redirect('home')
