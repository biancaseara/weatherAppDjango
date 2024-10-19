import datetime
import requests
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings

# Create your views here.
def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'valença'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f'https://www.googleapis.com/customsearch/v1?key={settings.SEARCH_ENGINE_API_KEY}&cx={settings.SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge'

    data = requests.get(city_url).json()
    print(f'data = {data}') # For debugging purposes
    search_items = data.get('items')

    image_url = 'https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
    if search_items and len(search_items) > 1:
        image_url = search_items[1]['link']

    try:
        response = requests.get(url)
        data = response.json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

        day = datetime.date.today()
        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url,
        })
    
    except Exception as e:
        print(e)  # For debugging purposes
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()

        return render(request, 'index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'valença',
            'exception_occurred': exception_occurred,
            'image_url': None,
        })
