#encoding:utf-8
from django.forms import ModelForm
from django import forms
from models import *

class fcarrito(ModelForm):
    class Meta:
        model=carrito
        exclude=['producto','id_sesion','estado']



class ubicacion_form(ModelForm):
	class Meta:
		model=ubicacion


class cantidad_form(ModelForm):
	class Meta:
		model=model_reserva_producto


class Form_logueo(ModelForm):
	class Meta:
		model = model_usuarios
		fields=["cargo","clave"]

class clienteform(ModelForm):
 	class Meta:
 		model=cliente
class form_entrada(ModelForm):
	class Meta:
		model=Entrada

class Form_registro_distri(ModelForm):
	class Meta:
		model = model_usuarios

class Form_registro_cate(ModelForm):
	class Meta:
		model = model_categoria	
class Form_registro_produc(ModelForm):
	class Meta:
		model = model_producto
class Form_proveedor(forms.ModelForm):
	class Meta:
		model = model_proveedor

class Form_producto(forms.ModelForm):
	class Meta:
		model = model_producto
class Form_almacen(forms.ModelForm):
	class Meta:
		model = model_almacen
class Form_cantidad(forms.ModelForm):
	class Meta:
		model = model_reserva_producto

class form_compra(forms.ModelForm):
	class Meta:
		model = compra
