
#!pip3 install twilio

import os
import re
from pandas.io import feather_format 
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import pandas as pd 
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from datetime import datetime



query = 'cadiz'
api_key = API_KEY_WAPI

url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&day=1&aqi=no&alert=no'


response = requests.get(url_clima).json()

# print(json.dumps(response, indent=4))
# print(response)
# print(response.keys()) #dict_keys(['location', 'current', 'forecast'])

# print(response['forecast']['forecastday'][0].keys())
#print(response['forecast']['forecastday'][0]['hour'])
# print(len(response['forecast']['forecastday'][0]['hour']))


# fecha = response['forecast']['forecastday'][0]['hour'][1]['time'].split()[0]
# hora = int(response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1].split(':')[0])
# condiciones = response['forecast']['forecastday'][0]['hour'][0]['condition']['text']
# temperatura = response['forecast']['forecastday'][0]['hour'][0]['temp_c']
# willrain = int(response['forecast']['forecastday'][0]['hour'][0]['will_it_rain'])
# probabilidadlluvia = response['forecast']['forecastday'][0]['hour'][0]['will_it_rain']


# print("la fecha es {}".format(fecha))
# print("la hora es {}".format(hora))
# print("las condiciones es {}".format(condiciones))
# print("la temperatura es de {} grados".format(temperatura))

# if willrain == 0:
#     print("NO VA A LLOVER HOY!! la probabilidad de luevia es {}%".format(probabilidadlluvia))
# else:
#     print("HOY LLOVERA!! coge el paraguas, la probabilidad de luevia es {}%".format(probabilidadlluvia))
    


#definimos la funcion que nos devolvera los resultados del tiempo por hora
def get_forecast(response, i):
        
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condiciones = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    willrain = int(response['forecast']['forecastday'][0]['hour'][i]['will_it_rain'])
    probabilidadlluvia = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    
    return fecha,hora,condiciones,temperatura,willrain,probabilidadlluvia


# declaramos la lista y la rellenemos con un bucle for --> habra un total de 24 registros
datos = []
 
for i in tqdm (range(len(response['forecast']['forecastday'][0]['hour'])), colour = 'green'):
    
    datos.append(get_forecast(response, i))
   

# print(datos)

#vamos a declarar el data set
col = ['fecha', 'hora', 'Condiciones', 'temperatura', 'lluvia', 'probabilidadlluvia']
#col = {'fecha':'Fecha', 'hora':'Hora', 'Condiciones':'Condiciones', 'temperatura':'Temperatura', 'willrain':'Luvia', 'probabilidadlluvia':'Prob_lluvia'}
df = pd.DataFrame(datos,columns = col)
#print(df)

df_rain = df[(df['lluvia'] == 0) & (df['hora'] > 7) & (df['hora'] < 23)]
df_rain = df_rain[['hora','Condiciones']]
df_rain.set_index('hora', inplace = True)
#print(df_rain)


#conexion a twilio y mensaje

time.sleep(2)
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                    body =  '\n Hola!! \n\n\n El pronostico de lluvia hoy ' + df['fecha'][0] + ' en ' + query + ' es:  \n\n\n' + str(df_rain),
                    from_=PHONE_NUMBER,
                    to='+34640325655')

print('mensaje enviado' + message.sid)