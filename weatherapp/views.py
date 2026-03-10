
from django.shortcuts import render, redirect
from .models import City
import requests

def home(request):

    api_key = "ede35d1a85b55b5992cfb1403c"

    if request.method == "POST":
        city_name = request.POST.get("city")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

        data = requests.get(url).json()

        if data.get("cod") != 200:
            return render(request, "weatherapp/index.html", {"error": "City not found"})

        if not City.objects.filter(name=city_name).exists():
            City.objects.create(name=city_name)

        return redirect("/")

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}&units=metric"
        data = requests.get(url).json()

        weather_data.append({
            "city": city.name,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        })

    context = {"weather_data": weather_data}

    return render(request, "weatherapp/index.html", context)