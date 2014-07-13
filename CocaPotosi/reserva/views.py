from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
import ho.pisa as pisa
import cStringIO as StringIO
from django.template.loader import render_to_string
#from django.contrib.contenttypes.models import ContentType
import cgi
from datetime import date,timedelta,datetime,time
import pdb

from CocaPotosi.apps.principal.models import *
from reserva.models import *
from reserva.form import *
from django.core.urlresolvers import reverse

def confirmar (request):
 	return render_to_response('reservas/confirmar.html',{},RequestContext(request))


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

def reporteFiltro(request):
    if request.method == "POST":
        tipo = request.POST["sopcion"]
        if tipo == "1":
            f = request.POST["tfecha"]
            busqueda=Reserva.objects.get(fecha_reserva=f)
            #return HttpResponse(f)
            #busqueda = (
             #   Q(fecha_reserva__icontains=f))
            usuarios = cliente.objects.all()
            ventas = Reserva.objects.filter(busqueda)
            #print  ventas
            #return HttpResponse(ventas.count)
            html = render_to_string('reservas/pdf_almacen.html', {'pagesize': 'A4', 'ventas': ventas, 'usuarios': usuarios},
                                    context_instance=RequestContext(request))
            return generar_pdf(html)
        if tipo == "2":
            productos = model_producto.objects.all()
            stock = model_almacen.objects.all()
            html = render_to_string('reservas/pdf_almacen.html', {'pagesize': 'A4', 'productos': productos, 'stock': stock},
                            context_instance=RequestContext(request))
            return generar_pdf(html)
        if tipo == "3":
            usuarios = cliente.objects.all()
            ventas = Reserva.objects.all()
            html = render_to_string("reservas/pdf_detalle.html", {'pagesize': 'A4', 'ventas': ventas, 'usuarios': usuarios},
                                    context_instance=RequestContext(request))
            return generar_pdf(html)
    else:
        return HttpResponseRedirect("/entrar/")


def seleccion(request):
    if request.method == 'POST' :
        formulario = fechasForm(request.POST)
        if formulario.is_valid():
            #cic = request.POST['ciclo']
            #mun = request.POST['municipio']
            fecha_ini = request.POST['fecha_ini']
            fecha_fin = request.POST['fecha_fin']
            anho_ini = datetime.strptime(fecha_ini, "%d/%m/%Y").strftime("%Y")
            mes_ini = datetime.strptime(fecha_ini, "%d/%m/%Y").strftime("%m")
            dia_ini = datetime.strptime(fecha_ini, "%d/%m/%Y").strftime("%d")
            anho_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").strftime("%Y")
            mes_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").strftime("%m")
            dia_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").strftime("%d")
            return HttpResponseRedirect(reverse(detalle_calendario, args=(dia_ini, mes_ini, anho_ini, dia_fin, mes_fin, anho_fin)))
    else:
        formulario = fechasForm()
    return  render_to_response('reservas/selec_fechas.html', {
        'formulario' :formulario,
    }, context_instance=RequestContext(request))

def detalle_calendario(request, dia_ini, mes_ini, anho_ini, dia_fin, mes_fin, anho_fin):
    fecha_ini =  date(int(anho_ini), int(mes_ini), int(dia_ini))
    fecha_fin = date(int(anho_fin), int(mes_fin), int(dia_fin))
    #pdb.set_trace()
    grupa = Reserva.objects.filter(fecha_reserva__lte= fecha_fin,fecha_reserva__gte=fecha_ini).order_by('fecha_reserva')
    detalles = DetalleReserva.objects.all()
    
    return render_to_response('reservas/det_cal.html',{'detalles':detalles,'ga':grupa,"dia_ini":dia_ini,"mes_ini":mes_ini,"anho_ini":anho_ini,"dia_fin":dia_fin,"mes_fin":mes_fin,"anho_fin":anho_fin}, context_instance = RequestContext(request))

def factura(request,id):
	hoy = datetime.now().date()
	res=get_object_or_404(Reserva,pk=id)
	detres=get_object_or_404(DetalleReserva,reserva=res.id)
	#pdb.set_trace()
	fac = Factura()
	fac.idreserva = res
	fac.save()
	f=get_object_or_404(Factura,idreserva=res.id)
	p_uni=detres.precio/detres.cantidad
	
	html=render_to_string("reservas/factura.html",{'f':f,'p_uni':p_uni,'pagesize':'A4',"res":res,"detres":detres,'hoy':hoy},context_instance=RequestContext(request))
	return generar_pdf(html)

def generar_pdf(html):
	resultado=StringIO.StringIO()
	pdf=pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")),resultado)
	if not pdf.err:
		return HttpResponse(resultado.getvalue(),mimetype='application/pdf')
	return HttpResponse("Error en generar el pdf")


