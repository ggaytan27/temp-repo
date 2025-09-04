#Librerias
import win32com.client as win32
import os
import time
from config import EMAIL, SUBJECT, API_KEY_WAPI, PROXI_USER, PROXI_PWD, PROXIES
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import pandas as pd
import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime

def request_weather_api(api_key, query, proxies, auth):
    url = "http://api.weatherapi.com/v1/forecast.json?key="+api_key+"&q="+query+"&days=1&aqi=no&alerts=no"
    try:
        response = requests.get(url, proxies=proxies, auth=auth).json()
    except:
        print(f"Error: {response.status_code}, {response.text}")
    
    return response

def get_forecast(response, i, weather_translate):
    date = response['forecast']['forecastday'][0]['date'] #fecha
    maxTemp= response['forecast']['forecastday'][0]['day']['maxtemp_c'] #maxtemp
    minTemp= response['forecast']['forecastday'][0]['day']['mintemp_c'] #mintemp
    chanceRain = response['forecast']['forecastday'][0]['hour'][0]['chance_of_rain'] #Posbilidad de lluvia
    weatherCondition = response['forecast']['forecastday'][0]['day']['condition']['text'] #condicion clima

    weatherConditionTranslate = weather_translate[weatherCondition]

    if not weatherConditionTranslate:
        weatherConditionTranslate = weatherCondition
    
    mensaje = 'Hola, este es el pronostico del clima del dia de hoy: ' + date + '\nTemperadura Maxima: '+ str(maxTemp) +' °C\nTemperadura Minima: '+ str(minTemp) +' °C\nPosibilidad de Lluvia: '+ str(chanceRain) + '%' +'\nCondicion: '+ str(weatherConditionTranslate)
    
    return mensaje    

def send_email(mensaje):
    try:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.TO = EMAIL
        mail.Subject = SUBJECT
        mail.Body = mensaje
        mail.Send()
        print("Email enviado exitosamente")
    except:
        print(e)