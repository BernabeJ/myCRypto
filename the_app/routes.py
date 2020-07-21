from the_app import app
from flask import render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from forms import CompraForm, Status
from datetime import date, time
import requests
import json



SECRET_KEY=app.config['SECRET_KEY'] 

@app.route("/")
def index():
    conn = sqlite3.connect(app.config['BASE_DATOS'])
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
    Key = app.config['KEY']
    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
    lista = ['EUR', 'BTC','ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX' ]
    form = CompraForm(request.form)
    cryptos = ('EUR', 'BTC','ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX' )
    conn = sqlite3.connect(app.config['BASE_DATOS'])
    cur = conn.cursor()
    d={}
    for key in d:   
        Key = app.config['KEY']
        URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
        respuesta = requests.get(URL.format(request.values.get("Q"), request.values.get("From"),request.values.get("To"),Key))
        json = respuesta.json()
    for key in cryptos:   
        consultacrypto = "SELECT sum(to_quantity) from movimientos WHERE to_currency ='{}'"
        respuesta = (consultacrypto.format(key))
        cantidad_comprada = cur.execute(respuesta).fetchall()
        cantidad_comprada = cantidad_comprada[0]
        consultacrypto = "SELECT sum(form_quantity) from movimientos WHERE from_currency ='{}'"
        respuesta = (consultacrypto.format(key))
        cantidad_gastada = cur.execute(respuesta).fetchall()
        cantidad_gastada = cantidad_gastada[0]
        d[key] = cantidad_comprada[0]
        if cantidad_comprada[0] is not None or cantidad_gastada[0] is not None:
            if cantidad_comprada[0] is not None and cantidad_gastada[0] is not None:
                d[key] = cantidad_comprada[0] - cantidad_gastada[0]
            elif cantidad_comprada[0] == None and cantidad_gastada[0] is not None:
                d[key]= cantidad_gastada[0]
            else:
                d[key]=cantidad_comprada[0]       
                                                     
    if request.method == "GET":
        return render_template('compra.html', form=form, lista=lista)

    else:
        if form.validate():
            form = CompraForm(request.form)
            consulta = requests.get(URL.format(request.values.get("Q"), request.values.get("From"),request.values.get("To"),Key))
            json = consulta.json()
            price = (json["data"]["quote"])
            Q = float(request.form.get('Q'))
            
            for precio in price.values():
                precio = precio
                precio = round(precio['price'],4)

            if request.form.get('consultar'):
                form = CompraForm(request.form)
                precio_unitario = round(precio/Q,4)
                consulta_From = request.form.get('From')
                consulta_To = request.form.get('To')
                if consulta_From == consulta_To:
                    error_el=('No es posible  intercambiar {} por {}, por favor elija una seleccion correcta'.format(request.form.get('From'), request.form.get('To')))
                    return render_template('compra.html',  form=form, error_gral=False, lista=lista, error_el=error_el)
                if consulta_From == 'EUR' and consulta_To !='BTC':
                    error_int=("No es posible intercambiar EUR, por {} directamente. Solo se puede adquirir {}, con otras criptomonedas".format(request.form.get('To'),request.form.get('To')))
                    return render_template('compra.html',  form=form, error_gral=False, lista=lista, error_int=error_int)
                if consulta_From != 'BTC' and consulta_To == 'EUR':
                    error_int2=((" Sólo es posible intercambiar BTC por EUR. Si desea Eur por favor intecambia antes sus criptomonedas"))
                    return render_template('compra.html',  form=form, error_gral=False, lista=lista, error_int2=error_int2)
                else: 
                    return render_template('compra.html', precio=precio, form=form, error_gral=False,precio_unitario=precio_unitario, lista=lista)

            elif request.form.get('cancelar'):
                form = CompraForm(request.form)
                return render_template('compra.html', form=form, lista=lista)
            
            
            elif request.form.get('aceptar')   :
                consulta_From = request.form.get('From')
                consulta_To = request.form.get('To')
                cantidad = request.form.get('Q')
                cantidad = float(cantidad)
                tiempo = datetime.now()
                date = tiempo.date()
                time = tiempo.strftime("%H:%M:%S.%f")[:-3]
                precio_unitario = round (precio/Q,4) 
                eleccion = request.form.get('From')
                d[eleccion] = d[eleccion]
                valor = d.get(eleccion)
                if consulta_From == consulta_To:
                    error_el=('No es posible  intercambiar {} por {}, por favor elija una seleccion correcta'.format(request.form.get('From'), request.form.get('To')))
                    return render_template('compra.html',  form=form, error_gral=False, lista=lista, error_el=error_el)
                if consulta_From == 'EUR' and consulta_To !='BTC':
                    error_int=("No es posible intercambiar EUR, por {} directamente. Solo se puede adquirir {}, con otras criptomonedas".format(request.form.get('To'),request.form.get('To')))
                    return render_template('compra.html',  form=form, error_gral=False, lista=lista, error_int=error_int)
                if consulta_From != 'BTC' and consulta_To == 'EUR':
                    error_int2=((" Sólo es posible intercambiar BTC por EUR. Si desea Eur por favor intecambia antes sus criptomonedas"))
                    return render_template('compra.html',  form=form, error_gral=False, lista=lista, error_int2=error_int2)
            

                if request.form.get('From') == 'EUR' or request.form.get('From') != 'EUR'  and valor != None and  Q <= valor  :
                    query = "INSERT INTO movimientos (date, time, from_currency, form_quantity, to_currency, to_quantity, precio_unitario) values (?,?,?,?,?,?,?);"
                    datos = (date, time, request.form.get('From'), float(request.form.get('Q')) , request.form.get('To'), precio, precio_unitario)
                    cur.execute(query, datos)
                    conn.commit()
                    conn.close()
                    return redirect(url_for("index"))
                else:
                    sin_saldo=('Saldo insuficiente, consulte su saldo de {} y vuelva a intentarlo con otra cantidad'.format(request.form.get('From')))
                    return render_template('compra.html', form=form, error_gral=False, lista=lista, sin_saldo=sin_saldo)

        else:
            return render_template('compra.html', form=form, error_gral=False, lista=lista)

@app.route("/status" ,methods=["GET","POST"])
def status():
    form = Status(request.form)
    conn = sqlite3.connect(app.config['BASE_DATOS'])
    cur = conn.cursor()
    cryptos = ('BTC','ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX' )
    consultaEuros = "SELECT sum(form_quantity) from movimientos WHERE from_currency ='{}'"
    respuesta = (consultaEuros.format('EUR'))
    EurosInvertidos= cur.execute(respuesta).fetchall()
    EurosInvertidos=EurosInvertidos[0]
    EurosInvertidos= str(EurosInvertidos)[1:-2]

    d={}
    for key in d:   
        Key = app.config['KEY']
        URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
        respuesta = requests.get(URL.format(request.values.get("Q"), request.values.get("From"),request.values.get("To"),Key))
        json = respuesta.json()
    for key in cryptos:   
        consultacrypto = "SELECT sum(to_quantity) from movimientos WHERE to_currency ='{}'"
        respuesta = (consultacrypto.format(key))
        cantidad_comprada = cur.execute(respuesta).fetchall()
        cantidad_comprada = cantidad_comprada[0]
        consultacrypto = "SELECT sum(form_quantity) from movimientos WHERE from_currency ='{}'"
        respuesta = (consultacrypto.format(key))
        cantidad_gastada = cur.execute(respuesta).fetchall()
        cantidad_gastada = cantidad_gastada[0]
        d[key] = cantidad_comprada[0]
        if cantidad_comprada[0] is not None or cantidad_gastada[0] is not None:
            if cantidad_comprada[0] is not None and cantidad_gastada[0] is not None:
                d[key] = cantidad_comprada[0] - cantidad_gastada[0]
            elif cantidad_comprada[0] == None and cantidad_gastada[0] is not None:
                d[key]= cantidad_gastada[0]
            else:
                d[key]=cantidad_comprada[0]       
    conn.close()

    Saldo_E = []
   
    d = {k: v for k, v in d.items() if v!=None}

    for clave in d:
        Key = app.config['KEY']
        URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert=EUR&CMC_PRO_API_KEY={}"
        response = requests.get(URL.format(d[clave],clave,Key))
        json = response.json()
        print (json)
        Saldo_E.append(json.get('data').get('quote').get('EUR')['price'])
        Total_saldo=sum(Saldo_E)
        Total_saldo=round(Total_saldo,3)
            
    return render_template('status.html', form=form, Total_saldo=Total_saldo, EurosInvertidos=EurosInvertidos)

