from flask import render_template, redirect, url_for, flash, request
from . import venta
from app.extensions import db


#El index de ventas, lo que ve el usuario comprador al entrar
@venta.route("/inicio", methods=['GET'])
def inicio():

    return render_template("venta/ventasIndex.html")

#Secciones de pedidos y ajustes, cambian segun el usuario :p
@venta.route("/carrito", methods=['GET'])
def carrito():

    return render_template("venta/carrito.html")

@venta.route("/pedidos", methods=['GET'])
def pedidos():

    return render_template("venta/pedidos.html")

@venta.route("/pedido_detalle", methods=['GET'])
def pedido_detalle():

    return render_template("venta/pedido_detalle.html")

@venta.route("/pago", methods=['GET'])
def pago():

    return render_template("venta/pago.html")

@venta.route("/ajustes", methods=['GET'])
def ajustes():

    return render_template("venta/ajustes.html")

#aca va todo lo relacionado al catalogo y las divisiones segun el animal
@venta.route("/seleccionar_animal", methods=['GET'])
def seleccionar_animal():

    return render_template("venta/selector_animal.html")

@venta.route("/catalogo_cerdo", methods=['GET'])
def catalogo_cerdo():

    return render_template("venta/catalogo_cerdo.html")

@venta.route("/catalogo_pollo", methods=['GET'])
def catalogo_pollo():

    return render_template("venta/catalogo_pollo.html")

@venta.route("/catalogo_res", methods=['GET'])
def catalogo_res():

    return render_template("venta/catalogo_res.html")