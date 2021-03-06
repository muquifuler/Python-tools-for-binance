from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import *
from twisted.internet import reactor

import keyboard
import pandas as pd
import time

# Your credentials
api_key=''; 
secret_key='';

client = Client(api_key, secret_key)
keyboard.on_press_key("q", lambda _: reactor.stop() )

msg = None
print("--------------Staking Mode--------------")
cripto = input("Ej: ETHUSDT XTZUSDT ADAUSDT BNBUSDT, etc --> ")

def calculoStaking(msg):
    cantidad = int(input("¿Cantidad? "))
    porcentajeAnual = int(input("¿Porcentaje anual? "))
    dias = int(input("¿A cuantos dias? "))
    porcentajeRealDeGanancia = (dias*porcentajeAnual)/365
    gananciaEnCripto = (porcentajeRealDeGanancia*cantidad)/100
    valorActual = msg['b']
    valorActual = valorActual[:-9]
    gananciaEnDolar = gananciaEnCripto*int(valorActual)
    print(f"Ganarás {gananciaEnCripto} {cripto}, {gananciaEnDolar} USDT")
    print(f"Ganancia por dia {gananciaEnCripto/dias} {cripto}, {gananciaEnDolar/dias} USDT")
    reactor.stop()



bm = BinanceSocketManager(client)
bm.start_symbol_ticker_socket(cripto, calculoStaking)
bm.start()

