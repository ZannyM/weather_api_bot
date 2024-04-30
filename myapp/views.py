from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .weatherapi import get_weather
from myapp import *
from dotenv import load_dotenv
import os
from twilio.rest import Client
import datetime


'''{'cloud_pct': 0, 'temp': 11, 'feels_like': 10, 
'humidity': 62, 'min_temp': 9, 'max_temp': 13, 'wind_speed': 0, 
'wind_degrees': 0, 'sunrise': 1714451467, 'sunset': 1714491522}'''
'''

### City
- Temperature: 7°C
- Feels Like: 2°C
- Humidity: 87%
- Cloud Cover: 75%

### Sun
- Sunrise: 06:32 AM
- Sunset: 06:41 PM

'''
# Create your views here.
def message_send(twilio_number,user_number,message):
        account_sid = os.environ.get("ACCOUNT_SID")
        auth_token = os.environ.get("AUTH_TOKEN")
        client = Client(account_sid,auth_token)

        client.messages.create(
            from_=twilio_number,
            to=user_number,
            body=message
        )

def get_suninfo(unix_timestamp):
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
    time = timestamp.strftime("%I:%M%p")   #output 06:32 AM
    return time
    

@csrf_exempt
def home(request):

    load_dotenv()
  
    TWILID_PHONE_NUMBER = os.environ.get("TWILID_PHONE_NUMBER")
    if request.method == "POST":
        message = request.POST
        
        user_name = message["ProfileName"]
        user_number = message["From"]
        the_Message = message["Body"]

        if the_Message.lower() in ['hey','hello','hi','hy','hei']:
            message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number, f"📌 Welcome to todays weather forecast  --{user_name}--")
        
        elif "weather" in the_Message.lower():

            city = the_Message[7: ].strip()
            forecast = get_weather(city)
            if isinstance(forecast,str):
                message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number, forecast)
            if city is None:
                print("City does not exist")
            else:
                if forecast is not None:
                    temperature = forecast.get('temp')
                    feeling = forecast.get('feels_like')
                    humidity = forecast.get('humidity')

                    sunrise_unix = forecast.get('sunrise')
                    sunrise = get_suninfo(sunrise_unix)

                    sunset_unix = forecast.get('sunset')
                    sunset = get_suninfo(sunset_unix)

                    cloud_cover = forecast.get('cloud_pct')
                    if cloud_cover == 0:
                        message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number ,f"### Weather for the Day\n\n### City: {city}\n- Temparature: {temperature}°C \n- Feels Like: {feeling}°C \n- Humidity: {humidity} \n- Cloud Cover: {cloud_cover}% ☀️\n\n### Sun\n- Sunrise: {sunrise}\n- Sunset: {sunset}")
                    elif cloud_cover >=11 or cloud_cover <= 25:
                        message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number ,f"### Weather for the Day\n\n### City: {city}\n- Temparature: {temperature}°C \n- Feels Like: {feeling}°C \n- Humidity: {humidity} \n- Cloud Cover: {cloud_cover}% 🌤️\n\n### Sun\n- Sunrise: {sunrise}\n- Sunset: {sunset}")
                    elif cloud_cover >=25 or cloud_cover <= 50:
                        message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number ,f"### Weather for the Day\n\n### City: {city}\n- Temparature: {temperature}°C \n- Feels Like: {feeling}°C \n- Humidity: {humidity} \n- Cloud Cover: {cloud_cover}% 🌥️\n\n### Sun\n- Sunrise: {sunrise}\n- Sunset: {sunset}")
                    elif cloud_cover >= 51 or cloud_cover <= 75:
                        message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number ,f"### Weather for the Day\n\n### City: {city}\n- Temparature: {temperature}°C \n- Feels Like: {feeling}°C \n- Humidity: {humidity} \n- Cloud Cover: {cloud_cover}% ☁️\n\n### Sun\n- Sunrise: {sunrise}\n- Sunset: {sunset}")
                    elif cloud_cover >= 76 or cloud_cover <= 100:
                        message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number ,f"### Weather for the Day\n\n### City: {city}\n- Temparature: {temperature}°C \n- Feels Like: {feeling}°C \n- Humidity: {humidity} \n- Cloud Cover: {cloud_cover}% 🌧️\n\n### Sun\n- Sunrise: {sunrise}\n- Sunset: {sunset}")
                    else:
                        message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number ,f"### Weather for the Day\n\n### City: {city}\n- Temparature: {temperature}°C \n- Feels Like: {feeling}°C \n- Humidity: {humidity} \n- Cloud Cover: {cloud_cover}% ☀️\n\n### Sun\n- Sunrise: {sunrise}\n- Sunset: {sunset}")
                else:
                    message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number,"⚠️ Forecast Does not exist: \n Enter a Valid City")


        else:
            message_send(f'whatsapp:{TWILID_PHONE_NUMBER}',user_number,"⚠️ You have entered the incorrect city name")
            
            

    return render(request, 'home.html')
