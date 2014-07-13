#encoding:utf-8
from django import forms

class CantidadForm(forms.Form):
	cantidad = forms.IntegerField(label="Cantidad de Producto")

class fechasForm(forms.Form):
   
    fecha_ini = forms.DateField(label="Fecha Inicio", help_text="Dia/Mes/Año")
    fecha_fin = forms.DateField(label="Fecha Finalización", help_text="Dia/Mes/Año")