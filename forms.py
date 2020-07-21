from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length
from flask import request
import sqlite3
import run




#def compras_posibles(form,field):
    #if field.data != "BTC" and form.From.data == "EUR":
        #raise ValidationError("No es posible intercambiar EUR, por {} directamente. Solo se puede adquirir {}, con otras criptomonedas".format(field.data,field.data))
    #elif field.data == "EUR" and form.From.data != "BTC":
        #raise ValidationError(" Sólo es posible intercambiar BTC por EUR. Si desea Eur por favor intecambia antes sus criptomonedas")


def comprueba_Q(form, field):
    
    if field.data <=0:
        raise ValidationError("Por favor, ingrese un valor positivo y superior a 0")

class CompraForm(FlaskForm):    
    cryptos = ('EUR', 'BTC','ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX' )
    From =  SelectField(label='From: ', choices=[(moneda,moneda)for moneda in cryptos])
    To =  SelectField(label='To: ', choices=[(moneda,moneda)for moneda in cryptos])
    Q = FloatField('Cantidad:', validators=[DataRequired("debe de introducir una cantidad valida"),comprueba_Q])
    Q2 = FloatField('Cantidad: ')
    PU = FloatField('Precio Unitario: ')
    consultar = SubmitField('Consultar')    
    aceptar = SubmitField('√')
    cancelar = SubmitField('X')

class Status(FlaskForm):
    
    invertido = FloatField('Invertido: ')
    valor_actual = FloatField('Valor actual: ')
  

