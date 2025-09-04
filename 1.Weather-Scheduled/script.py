"""
************************************************************************
* Author = @ggaytan                                                    *
* Date = '30/09/2024'                                                  *
* Description = Envio de pronostico del clima via email                *
************************************************************************
"""

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

from utils import request_weather_api, get_forecast, send_email

#Variables
weather_translate = {
    'Sunny' : 'Soleado',
    'Rain' : 'Lluvia',
    'Cloudy' : 'Nublado',
    'Parthly Cloudy' : 'Parcialmente Nublado',
    'Wind' : 'Viento',
    'Storm' : 'Tormenta',
    'Snow' : 'Nieve'
}

query = 'Juarez'
api_key = API_KEY_WAPI
proxies = PROXIES
auth = HttpNtlmAuth(PROXI_USER, PROXI_PWD)


response = request_weather_api(api_key, query, proxies, auth)


for i in tqdm(range(24), colour = 'green'):
    mensaje = get_forecast(response, i, weather_translate)


send_email(mensaje)

