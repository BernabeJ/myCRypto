from the_app import app
from flask import render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from forms import CompraForm, Status
import os
from datetime import date, time
import requests
import json

BASE_DATOS = "./data/crypto.db"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")
def index():
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()
    query = "SELECT id, date, time, from_currency, form_quantity, to_currency, to_quantity, precio_unitario FROM movimientos;"
    comprados = cur.execute(query).fetchall()
    comprueba_reg = ('SELECT * FROM movimientos')
    reg = cur.execute(comprueba_reg).fetchall()
    conn.close()

    if len(reg) == 0:
        return render_template('index0.html')

    else:
        return render_template('index.html', comprados=comprados)


@app.route("/compra", methods=["GET", "POST"])
def compra():
    Key = "a7e9eca5-c06a-48e5-847c-8e8daab8d980"
    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
    lista = ['EUR', 'BTC','ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX' ]
    form = CompraForm(request.form)
    if request.method == "GET":
        return render_template('compra.html', form=form, lista=lista)

    else:
        if form.validate():
            form = CompraForm(request.form)
            consulta = requests.get(URL.format(request.values.get("Q"), request.values.get("From"),request.values.get("To"),Key))
            json = consulta.json()
            conn = sqlite3.connect(BASE_DATOS)
            cur = conn.cursor()
            price = (json["data"]["quote"])
            Q = float(request.form.get('Q'))
            for precio in price.values():
                precio = precio
                precio = round(precio['price'],4)

            if request.form.get('consultar'):
                form = CompraForm(request.form)
                precio_unitario = round(precio/Q,4) 
                return render_template('compra.html', precio=precio, form=form, precio_unitario=precio_unitario, lista=lista)

            elif request.form.get('cancelar'):
                form = CompraForm(request.form)
                return render_template('compra.html', form=form, lista=lista)

            elif request.form.get('aceptar'):     
                tiempo = datetime.now()
                date = tiempo.date()
                time = tiempo.strftime("%H:%M:%S.%f")[:-3]
                precio_unitario = round (precio/Q,4) 
                print(precio_unitario)
                print (precio)
                query = "INSERT INTO movimientos (date, time, from_currency, form_quantity, to_currency, to_quantity, precio_unitario) values (?,?,?,?,?,?,?);"
                datos = (date, time, request.form.get('From'), request.form.get('Q'), request.form.get('To'), precio, precio_unitario)
                
                cur.execute(query, datos)
                conn.commit()
                conn.close()

                return redirect(url_for("index"))

        else:
            return render_template('compra.html', form=form, error_gral=False, lista=lista)

@app.route("/status" ,methods=["GET","POST"])
def status():
    form = Status(request.form)
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()

    
    consultasaldo = "SELECT sum(to_quantity) from movimientos WHERE from_currency='EUR'"
    compraEuros = cur.execute(consultasaldo).fetchall()
    compraEuros = compraEuros[0]

    consultasaldo = "SELECT sum(to_quantity) from movimientos WHERE to_currency = 'EUR'" 
    invierteEuros = cur.execute(consultasaldo).fetchall()
    IEuro = invierteEuros[0]

    Monedas = ('EUR', 'BTC','ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX' )

    d = {}
    for moneda in Monedas:
        consultacrypto = "SELECT sum(to_quantity) from movimientos WHERE from_currency ='{}'"
        compraCrypto = cur.execute(consultacrypto).fetchall()
        compracrypto = compraCrypto[0] 

        consultacrypto = "SELECT sum(form_quantity) from movimientos WHERE from_currency ='{}'"
        invierteCrypto = cur.execute(consultacrypto).fetchall()
        ICrypto = invierteCrypto[0]

        if compracrypto[0] or ICrypto[0] is not None:
            if compracrypto[0] and ICrypto[0] is not None:
                d[moneda] = compracrypto[0] + ICrypto[0]
                            
            elif compracrypto[0] == None and ICrypto[0] is not None:
                d[moneda] = ICrypto[0]
                            
            else:
                d[moneda] = compracrypto[0]

                    
        for key in d:
                        
            Key = "a7e9eca5-c06a-48e5-847c-8e8daab8d980"
            URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
            respuesta = requests.get(URL.format(d.get(key),key, Key))
            json = respuesta.json()
            print (json)
            print (d)


        return render_template('status.html', form=form, compraEuros=compraEuros, inversion_Euros=IEuro)

