from django.db import models
from CocaPotosi.apps.principal.models import *

class Reserva(models.Model):
	fecha_reserva = models.DateField(auto_now_add=True)
	precio_total = models.FloatField(default=0)
	cliente = models.ForeignKey(cliente)
	estado = models.BooleanField(default=False)
	def __unicode__(self):
		return self.cliente.nombre

class DetalleReserva(models.Model):
	reserva = models.ForeignKey(Reserva)
	cantidad = models.IntegerField(default=0)
	precio = models.FloatField(default=0)
	producto = models.ForeignKey(model_producto)
	def __unicode__(self):
		return self.producto.nombre

class Factura(models.Model):
	idreserva = models.ForeignKey(Reserva)
	def __unicode__(self):
		return self.idreserva
