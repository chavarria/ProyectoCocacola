from django import forms

class CantidadForm(forms.Form):
	cantidad = forms.IntegerField(label="Cantidad de Producto")