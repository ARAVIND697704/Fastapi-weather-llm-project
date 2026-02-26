import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY= os.getenv("WEATHER_API_KEY")

def get_weather(city:str):
    url="https://api.openweathermap.org/data/2.5/weather"

    params={
        "q": city,
        "appid":WEATHER_API_KEY,
        "units":"metric"
    }

    response=requests.get(url,params=params)

    if response.status_code!=200:
        return None
    
    data=response.json()

    return{
        "temperature":data["main"]["temp"],
        "condition":data["weather"][0]["description"]
    }