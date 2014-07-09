from django.shortcuts import render,render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse 
from forms import *

from models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm
from django.core.context_processors import csrf
import time
from calendar import month_name
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.timesince import timesince
def mapa(request):
    formulario=ubicacion_form()
    return render_to_response('mapa.html',{"form":formulario},context_instance=RequestContext(request))


class FormularioComentario (ModelForm):
    class Meta:
        model=Comentario
        exclude=["identrada"]

def poncomentario (request,pk):
    p = request.POST
    if 'mensaje' in p:
        autor = "Anonimo"
        if p["autor"]: autor =p["autor"]

        comentario=Comentario(identrada=Entrada.objects.get(pk=pk))
        cf= FormularioComentario(p,instance = comentario)
        cf.fields["autor"].required=False

        comentario=cf.save(commit=False)
        comentario.autor = autor
        comentario.save()
    return HttpResponseRedirect(reverse("CocaPotosi.apps.principal.views.entrada",args=[pk]))
    
def mkmonth_lst():    
    if not Entrada.objects.count(): return[]

    year, month = time.localtime()[:2]
    first  = Entrada.objects.order_by("fecha")[0]
    fyear = first.fecha.year
    fmonth = first.fecha.month
    months = []

    for y in range(year,fyear-1,-1):
        start,end = 12,0
        if y ==year:start = month
        if y == fyear: end = fmonth -1

        for m in range(start,end,-1):
            months.append((y,m,month_name[m]))



    return months
    
def month (request,year,month):
    entrada = Entrada.objects.filter(fecha__year= year, fecha__month= month)
    return render_to_response("listado.html",dict(entrada_list=entrada, user= request.user,month= mkmonth_lst(),archive=True))
    
def entrada (request, pk):
    identrada = Entrada.objects.get(pk=int(pk))
    comentario = Comentario.objects.filter(identrada=identrada)
    d = dict(entrada=identrada, comentario=comentario, form=FormularioComentario(),usuario= request.user)
    d.update(csrf(request))
    return render_to_response("entrada.html",d)
    
def main(request):
    entrada = Entrada.objects.all().order_by("-fecha")
    paginator = Paginator(entrada,3)
    try: pagina = int (request.GET.get("page",'1'))
    except ValueError : pagina = 1
    try:
        entrada = paginator.page(pagina)
    except(InvalidPage, EmptyPage):
        entrada = paginator.page(paginator.num_pages)
    return render_to_response("listado.html",dict(entrada = entrada, usuario = request.user, entrada_list= entrada.object_list, months= mkmonth_lst))



# pagina de inicio
def inicio (request):
	return render_to_response('index0.html',{},RequestContext(request))
def home (request):
    if request.method=='POST':
        formu=clienteform(request.POST)
        if formu.is_valid():
            formu.save()
            return HttpResponseRedirect('reserva/productos/select/',{},RequestContext(request))
    else:
        formu=clienteform()
    return render_to_response('regiscliente.html',{'formu':formu},context_instance=RequestContext(request))

def view_logueo(request):
    if request.method == 'POST':
        formulario = Form_logueo(request.POST)        
        if formulario.is_valid:
            usuario = request.POST['cargo']
            contra = request.POST['clave']            
            if model_usuarios.objects.filter(cargo=usuario,clave=contra):            	
             	request.session['usuario'] = usuario            	
                 #formulario = Regis_admin.objects.filter(cargo=usuario,clave=contra)
                formulario = model_usuarios.objects.get(cargo=usuario)
                if formulario.id == 1:
                 #print (formulario.id)
                     titulo = "estructura.html"
            	    
                else:   
                     titulo = "estructura1.html"
                 #print (titulo)
                return HttpResponseRedirect('/index')
                 #return render_to_response('admin.html',{'formulario':formulario,'titulo':titulo}, context_instance=RequestContext(request))
                    
            else:
             	return render_to_response('nousuario.html', context_instance=RequestContext(request))        
        else:
        	return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = Form_logueo()
    return render_to_response('login.html',{'formulario':formulario}, context_instance=RequestContext(request))


def index(request):
 	return render_to_response('index1.html',{},RequestContext(request))


def cerrar(request):

	return HttpResponseRedirect('/')

def view_regis_distri(request):
                                            
            if request.method=='POST':                                                
                formulario = Form_registro_distri(request.POST, request.FILES)
                if formulario.is_valid():            
                    formulario.save()
                    return render_to_response('exito.html',{},RequestContext(request))
                else:
                    return render_to_response('error.html',{}, context_instance=RequestContext(request))                                        
            else:
                formulario = Form_registro_distri()
                return render_to_response('nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))

def view_ver_distri(request):
       
        formulario = model_usuarios.objects.all()     

        return render_to_response('ver_distribuidor.html',{'formulario':formulario}, context_instance=RequestContext(request))

def view_regis_cate(request):
	if request.method=='POST':                                                

		formulario = Form_registro_cate(request.POST, request.FILES)

		if formulario.is_valid():            
			formulario.save()
			return render_to_response('exito.html',{}, context_instance=RequestContext(request))
		else:
			return render_to_response('error.html',{}, context_instance=RequestContext(request))                                        
	else:
		formulario = Form_registro_cate()
		return render_to_response('regis_categoria.html',{'formulario':formulario}, context_instance=RequestContext(request))

def view_regis_proveedor(request):
    if request.method=='POST':                                                

        formulario = Form_proveedor(request.POST, request.FILES)

        if formulario.is_valid():            
            formulario.save()
            return render_to_response('exito.html',{},RequestContext(request))
        else:
            return render_to_response('error.html',{}, context_instance=RequestContext(request))                                        
    else:        
        formulario = Form_proveedor()
        return render_to_response('registro_proveedor.html',{'formulario':formulario}, context_instance=RequestContext(request))


def view_regis_produc(request):
    if request.method=='POST':
        formulario=Form_registro_produc(request.POST, request.FILES)        
        if formulario.is_valid():
            formulario.save()
            #foto = request.POST['fotografia']
            #print (foto)
            produc = model_producto.objects.all()
            for pro in produc:
                id_produc=pro.id
            #id_produc=1
            id_prove = request.POST['id_prove']
            cant_ent = request.POST['cant_entrada']
            #precio = request.POST['precio_sal']
            fecha = request.POST['fecha']
            almacen = model_almacen()
            almacen.cant_entra=cant_ent
            #num = request.POST['cant_entrada']
            #suma = int(num)
            #print(cant_ent)
            almacen.cant_sal=0
            almacen.fecha=fecha
            almacen.stock=request.POST['cant_entrada']
            almacen.id_produc_id=id_produc
            almacen.id_prove_id=id_prove
            almacen.save()
            return render_to_response('exito.html',{},RequestContext(request))
        else:
            return render_to_response('error.html',{},context_instance=RequestContext(request))
    else:
        categoria = model_categoria.objects.all()
        formulario = Form_registro_produc()
        dato = model_proveedor.objects.all()
        almacen = Form_almacen
        return render_to_response('regis_producto.html',{'almacen':almacen,'formulario':formulario,'proveedor':dato,'categoria':categoria},context_instance=RequestContext(request))

def productos(request):
    lista_productos=Producto.objects.all()
    return render_to_response("productos.html",{'lista_productos':lista_productos},context_instance=RequestContext(request))


def view_ver_producto(request):
           
        formulario = model_producto.objects.all()     

        return render_to_response('ver_producto.html',{'formulario':formulario}, context_instance=RequestContext(request))

def view_carrito(request):       
        formulario = model_reserva_producto.objects.all()     

        return render_to_response('mostrar.html',{'formulario':formulario}, context_instance=RequestContext(request))

def view_ver_cate(request):
       
        formulario = model_categoria.objects.all()     

        return render_to_response('ver_cate.html',{'formulario':formulario}, context_instance=RequestContext(request))
def reservar(request):
	formulario = model_categoria.objects.all()     
        return render_to_response('reserva.html',{'formulario':formulario}, context_instance=RequestContext(request))

def recuperar(request, id):
    datosp=model_producto.objects.filter(Q(id_cat = id))
   
    if request.method=='POST':
        formulario=Form_cantidad(request.POST)
        if formulario.is_valid():
            res = model_reserva_producto.objects.filter(Q(id_Usuario = formulario.cleaned_data["id_Usuario"]))
            if len(res)==0:
                formulario.save()
            return HttpResponseRedirect('/index')
    else:
        formulario=Form_cantidad()
    return render_to_response("mostrar.html",{"form":formulario,"formu":datosp},RequestContext(request))

def reservar_cantidad_producto(request):
    datosp=model_producto.objects.filter(Q(id_cat = id))
    return render_to_response("mostrar.html",{"formulario":datosp},RequestContext(request))
#pagina de listado de clientes
#@login_required(login_url='/ingresar')
def clientes(request):
	client=cliente.objects.all()
	return render_to_response('client.html',{'client':client},context_instance=RequestContext(request))
#pagina de modificar clientes

@login_required(login_url='/ingresar')
def modificarCliente(request,id):
	 client=get_object_or_404(cliente,pk=id)

	 if request.method=='POST':
	 	formu=clienteform(request.POST,instance=client)
	 	if formu.is_valid():
	 		formu.save()
	 		return HttpResponseRedirect('/cliente')
	 else:
	 	formu=clienteform(instance=client)
	 return render_to_response('modificar.html',{'formu':formu},context_instance=RequestContext(request))
def productos (request):
 	return render_to_response('productos.html',{},RequestContext(request))
def Promocion (request):
 	return render_to_response('promocion.html',{},RequestContext(request))
def noticias (request):
 	return render_to_response('noticias.html',{},RequestContext(request))
def acerca (request):
 	return render_to_response('acerca.html',{},RequestContext(request))

def add_product_view(request):
    info = "Inicializando"
    if request.method == "POST":
        form = addProductForm(request.POST,request.FILES)
        if form.is_valid():
            add = form.save(commit=False)
            add.status = True
            add.save() # Guardamos la informacion
            form.save_m2m()# Guarda las relaciones de ManyToMany
            info = "Datos creados con exito :)"
            return HttpResponseRedirect('/producto/%s'%add.id)
    else:
        form = addProductForm()
    ctx = {'form':form, 'informacion':info}
    return render_to_response('addProducto.html',ctx,context_instance=RequestContext(request))


def edit_product_view(request,id_prod):
    info = "Iniciando"
    prod = model_producto.objects.get(pk=id_prod)
    if request.method == "POST":
        form = addProductForm(request.POST,request.FILES,instance=prod)
        if form.is_valid():
            edit_prod = form.save(commit=False)
            form.save_m2m()
            edit_prod.status = True
            edit_prod.save() # Guardamos el objeto
            info = "Datos editados con exito :)"
            return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
    else:
        form = addProductForm(instance=prod)
    ctx = {'form':form,'informacion':info}
    return render_to_response('/editProducto.html',ctx,context_instance=RequestContext(request))

def view_regiscomentario(request):
    if request.method=='POST':
        formulario=form_entrada(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return render_to_response('exito.html',{},RequestContext(request))
        else:
            return render_to_response('error.html',{},context_instance=RequestContext(request))
    else:
        formulario=form_entrada()
        return render_to_response('regis_entrada.html',{'formulario':formulario},context_instance=RequestContext(request))

def addcarrito (request):
    if(request.session["idcompra"]==False):
        import hashlib
        request.session["idcompra"]=datetime.datetime.now().strftime("%y %m %d %H %M")
    if(request.method=="POST"):
        form=cantidad_form(request.POST)
        if (form.is_valid()):

            cantidad=request.POST["cantidad"]
            id_pro=request.POST["id_prod"]
            pro=model_producto.objects.get(id=id_pro)
            p=compra(idSession=request.session["idcompra"],cantidad=cantidad,id_pro=pro)
            p.save()
            lista=compra.objects.filter(idSession=request.session["idcompra"])
            listadetalle=[]
            total=0
            for item in lista:
                listadetalle.append({"item":item,"preciototal":item.cantidad*item.id_pro.precio})
                total=total+item.cantidad*item.id_pro.precio
            return render_to_response("mostrar.html",{"lista":listadetalle,"total":total},RequestContext(request))

def index3333(request):
    form=ubicacion_form()
    ubicaciones =ubicacion.objects.all().order_by('-fecha')

    return render_to_response('mapa.html',{'form':form,'ubicaciones':ubicaciones}, context_instance=RequestContext(request))


def coords_save(request):
    if request.is_ajax():
        form=ubicacion_form(request.POST)
        if form.is_valid():
            form.save()
            ubicaciones = ubicacion.objects.all().order_by('-fecha')

            data = '<ul>'
            for ubicacion in ubicaciones:
                data += '<li>%s %s %s</li>'% (ubicacion.nombre, ubicacion.user, ubicacion.fecha)

            data+='</ul>'
            
            return HttpResponse(simplejson.dumps({'OK': True, 'msg':'datos llenados correcamente'}),mimetype='application/json')
        else:
            return HttpResponse(simplejson.dumps({'OK': False,'msg':'debe llenar los datos'}), mimetype='application/json')


#de aqui el carrito

def carrito_mostrar(request):
    if not "contador" in request.session:
        request.session['contador']=0
    return HttpResponse(request.session['contador'])

def cargar_carrito(request,id):
    pro=model_producto.objects.get(id=int(id))
    fcarr=fcarrito()
    return render_to_response("fcarrito.html",{'fcarr':fcarr,'pro':pro},context_instance=RequestContext(request))

def listar_producto(request,id):
    pro=model_producto.objects.get(id=int(id))
    return render_to_response("productos_lista.html",{'producto':pro},context_instance=RequestContext(request))

def carrito_add(request,id):
    if request.method=="POST":
        cant=request.POST['cantidad']
        if int(cant)>0:
            if not "id_sesion"in request.session:
                request.sesion['id_sesion']=hashlib.md5(str(datetime.datetime.now())).hexdigest()
            pro=model_producto.objects.get(id=int(id))
            carr=carrito.objects.create(id_sesion=request.sesion["id_sesion"],estado=False,producto=pro,cantidad=int(cant))
            contador=request.session['contador']
            request.session['contador']=contador+1
    return HttpResponse(request.session['contador'])
def confirmar_compra(request):
    if request.user.is_autenticated():
        id_sesion=request.session["id_sesion"]
        carr=carrito.objects.filter(id_sesion=id_sesion)
        return render_to_response("confirmar_compra.html",{'carr':carr},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/ingresar/")

def eliminar_de_carrito(request,id):
    if "contador" in request.session:
        contador=request.session['contador']
        request.session['contador']=contador-1
        carr=carrito.objects.get(id=int(id))
        carr.delete()
        return HttpResponseRedirect("/confirmar/compra/")
    else:
        return HttpResponseRedirect("/productos/")
def realizar_transaccion(request):
    if request.user.is_autenticated():
        usuario=request.user
        u=User.objects.get(username=usuario)
        id_sesion=request.session["id_sesion"]
        carr=carrito.objects.filter(id_sesion=id_sesion)
        for i in carr:
            pre_total=float(i.producto.precio*i.cantidad)
            pro = model_producto.objects.get(id=i.producto.id)
            trans=pedido.objects.create(cliente=u,cantidad=i.cantidad, precio_total=pre_total)
            trans.producto.add(pro)
            trans.save()
            stock=pro.stock
            pro.stock=stock-i.cantidad
            pro.save()
        carr.delete()
        request.session["contador"]=0
        return HttpResponse("se realizo la transaccion")
    else:
        return HttpResponseRedirect("/ingresar/")

def compra(request):
    formulario = compra.objects.all()
    return render_to_response('mostrar.html',{'formulario':formulario}, context_instance=RequestContext(request))

