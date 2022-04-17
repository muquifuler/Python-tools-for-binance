# It is incomplete and I have no intention of finishing it, it is an old project
# If it doesn't work, it may be because in the binance web/manage API.
# the option restrict access for trusted IP addresses is enabled

# BINANCE BOT FOR UPTRENDS

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

a = 0
b = 0
c = 0
e = 0
numfinal = 0
subida = 0
bajada = 0
eth = pd.DataFrame(client.get_order_book(symbol="ETHUSDT"))
n = 0
nn = 0

cripto1 = input("Ej: ETHUSDT XTZUSDT ADAUSDT BNBUSDT --> ")

def salida():
    reactor.stop()

def wallet(msg):
    eth_balance = client.get_asset_balance(asset='ETH')
    xtz_balance = client.get_asset_balance(asset='XTZ')
    ada_balance = client.get_asset_balance(asset='ADA')
    bnb_balance = client.get_asset_balance(asset='BNB')
    usdt_balance = client.get_asset_balance(asset='USDT')
    beth_balance = client.get_asset_balance(asset='BETH')
    summ = float(eth_balance['free'])+float(beth_balance['free'])
    if (cripto1 == 'ETHUSDT'):
        UsdtTotal = (float(msg['b']) * float(summ))
    elif (cripto1 == 'XTZUSDT'):
        UsdtTotal = (float(msg['b']) * float(xtz_balance['free']))
    elif (cripto1 == 'ADAUSDT'):
        UsdtTotal = (float(msg['b']) * float(ada_balance['free']))
    elif (cripto1 == 'BNBUSDT'):
        UsdtTotal = (float(msg['b']) * float(bnb_balance['free']))
    else:
        pass
    print("            __________________   _______________   _______________   ______________   _______________")
    print(f"Tu wallet: |{summ} ETH+BETH| |{xtz_balance['free']} XTZ| |{ada_balance['free']} ADA| |{bnb_balance['free']} BNB| |{usdt_balance['free']} USDT|")
    print("Tus "+str(cripto1)+" en dolares son... "+str(UsdtTotal))
def prueba(msg):
    #Xprint(msg['q'])
    global n
    global nn
    global cripto1
    preciocomprapercent = msg['B']
    event_type = msg['e']
    change_percent = msg['p']
    numtotaldeintertrades = msg['n']

    media = f"Media actual: {msg['x']}"
    preciocompra = f"Precio Actual: {msg['b']}"

    wallet(msg)

    print(f"{media[:-6]}$")
    print(f"{preciocompra[:-6]}$")

    media = msg['x']
    preciocompra = msg['b']

    media = media[:-9]
    preciocompra = preciocompra[:-9]

    media = int(media)
    preciocompra = int(preciocompra)
#Comprar
    if (preciocompra <= media):
        p5ercent_media = ((media / 100) * 5)
        p5ercent_media_bajo = media - p5ercent_media
        if (preciocompra <= p5ercent_media_bajo):
            #TAKE PROFIT Orden compra
            print("Orden de Compra")
            cantidad = input("(x PARA CANCELAR)Cantidad a comprar: ")
            if (cantidad == "x" or cantidad == "X"):
                salida()
            else:
                buy_order = client.order_market_buy(symbol=cripto1, quantity=cantidad)
                print(buy_order)
        else:
            print(f"No es menor a 5%, se comprara a: {p5ercent_media_bajo}")
#Vender
    else:
        p3ercent_media = ((media / 100) * 3)
        p3ercent_media_alto = media + p3ercent_media
        if (preciocompra >= p3ercent_media_alto):
            if (n == 0 or nn == 0):
                print("Momento de vender")
                venta(cripto1)
                nn += 1
            else:
                print("Venta hecha")
        else:
            print(f"No es superior a 3%, se vendera a: {p3ercent_media_alto}")

def venta(cripto1):
    global n
    try:
        cantidad = input("(x PARA CANCELAR)Cantidad a vender: ")
        if (cantidad == "x" or cantidad == "X"):
            salida()
        else:
            sell_order = client.order_market_sell(symbol=cripto1, quantity=cantidad)
            print(sell_order)#IF MIN_NOTIONAL -> Numero de compra demasiado pequeño
            print(f"Se vendió por: {p3ercent_media_alto} o mas")
            n += 1             
    except BinanceAPIException as e:
        print(e)
    except BinanceOrderException as e:
        print(e)



bm = BinanceSocketManager(client)
bm.start_symbol_ticker_socket(cripto1, prueba)
bm.start()

#Detectar Tendencia Baja
#Detectar Tendencia Alta
