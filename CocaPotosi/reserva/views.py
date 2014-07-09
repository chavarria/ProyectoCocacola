from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

import ho.pisa as pisa
import cStringIO as StringIO
from django.template.loader import render_to_string
#from django.contrib.contenttypes.models import ContentType
import cgi


from CocaPotosi.apps.principal.models import *
from reserva.models import Reserva, DetalleReserva
from reserva.form import CantidadForm

def generarpdf(html):
	result = StringIO.StringIO()
	#links = Lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-16")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), mimetype='application/pdf')
	return HttpResponse('Error al Generar el PDF: %s' % cgi.escape(html))

def productos_reporte(request):
	productos = model_producto.objects.all()
	html = render_to_string('reservas/pdf_productos.html',{
			'productos':productos,
		}, context_instance=RequestContext(request))
	return generarpdf(html)

def reserva_reporte(request):
	reserva= Reserva.objects.all()
	productos = model_producto.objects.all()
	detallereserva = DetalleReserva.objects.filter(reserva = reserva)
	html = render_to_string('reservas/pdf_reserva.html',{
			'reserva':reserva,
		}, context_instance=RequestContext(request))
	return generarpdf(html)

def almacen_reporte(request):
	almacen= model_almacen.objects.all()
	productos = model_producto.objects.all()
	html = render_to_string('reservas/pdf_almacen.html',{
			'almacen':almacen,
		}, context_instance=RequestContext(request))
	return generarpdf(html)

def detalle_reporte(request):
	detalle= DetalleReserva.objects.all()
	productos = model_producto.objects.all()
	html = render_to_string('reservas/pdf_detalle.html',{
			'detalle':detalle,
		}, context_instance=RequestContext(request))
	return generarpdf(html)

def productos(request):
	productos = model_producto.objects.all()

	return render_to_response('reservas/index.html',{
			'productos':productos,
		},context_instance=RequestContext(request))


def clientes(request):
	clientes = cliente.objects.all().order_by('nombre')
	return render_to_response('reservas/select_cliente.html',{
			'clientes':clientes,
		},context_instance=RequestContext(request))

def create_reserva(request, cliente_id):
	r = Reserva.objects.create(
			cliente_id = cliente_id,
			precio_total = 0,
		)
	return HttpResponseRedirect('/reservas/seleccion/producto/'+str(r.id)+'/')

def select_productos(request, reserva_id):
	reserva = Reserva.objects.get(pk = reserva_id)
	productos = model_producto.objects.all()
	detallereserva = DetalleReserva.objects.filter(reserva = reserva)
	#select * from DetalleReserva where(reserva_id = reserva_id)
	return render_to_response('reservas/select_productos.html',{
			'reserva':reserva,
			'productos':productos,
			'detallereserva':detallereserva,
		},context_instance=RequestContext(request))

def cantidad(request, reserva_id, producto_id):
	reserva = Reserva.objects.get(pk=reserva_id)
	producto = model_producto.objects.get(pk = producto_id)
	a = model_almacen.objects.get(id_produc = producto)
	if request.method == 'POST':
		formulario = CantidadForm(request.POST)
		if formulario.is_valid():
			cantidad = formulario.cleaned_data['cantidad']
			precio_reserva = float(cantidad) * float(producto.precio)
			d = DetalleReserva.objects.create(
					producto_id = producto_id,
					reserva = reserva,
					cantidad = cantidad,
					precio = precio_reserva,
				)
			reserva.precio_total = reserva.precio_total + precio_reserva
			reserva.save()
			a.cant_sal = a.cant_sal + cantidad
			a.stock = a.stock - cantidad
			a.save()
			return HttpResponseRedirect('/reservas/seleccion/producto/'+str(reserva_id)+'/')
	else:
		formulario = CantidadForm()
	return render_to_response('reservas/cantidad_producto.html',{
		'formulario':formulario,
		'reserva':reserva,
		'producto':producto,
		'almacen':a,
		}, context_instance=RequestContext(request))