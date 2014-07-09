#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User




class model_usuarios(models.Model):
	ci=models.CharField(max_length=200)
	fotografia=models.ImageField(upload_to='img', verbose_name='imagen')	
	nombre=models.CharField(max_length=200)
	apellidos=models.CharField(max_length=200)
	cargo=models.CharField(max_length=200)
	clave=models.CharField(max_length=200)
	fecha=models.DateField(auto_now=True)
	def __unicode__(self):
	 	return "%s"%(self.ci)

class model_categoria(models.Model):
	nombre=models.CharField(max_length=200)
	descripcion=models.CharField(max_length=200)
	fecha=models.DateField(auto_now=True)
	id_admin=models.ForeignKey(model_usuarios)
	def __unicode__(self):
	 	return "%s"%(self.nombre)
		
class prueba(models.Model):
	ci=models.CharField(max_length=200)
	fotografia=models.ImageField(upload_to='img', verbose_name='imagen')	
	nombre=models.CharField(max_length=200)
	apellidos=models.CharField(max_length=200)
	cargo=models.CharField(max_length=200)
	clave=models.CharField(max_length=200)
	fecha=models.DateField()
	def __unicode__(self):
	 	return "%s"%(self.ci)

class model_proveedor (models.Model):
	usuario=models.CharField(max_length=200)
	nit=models.CharField(max_length=200)
	telefono=models.CharField(max_length=200)
	departamento=models.CharField(max_length=200)
	def __unicode__(self):
	 	return "%s"%(self.usuario)
	 	
class model_producto (models.Model):
	nombre=models.CharField(max_length=200)
	contenido_neto=models.CharField(max_length=200)
	sabor=models.CharField(max_length=200)
	fotografia=models.ImageField(upload_to='img', verbose_name='imagen')	
	precio=models.DecimalField(max_digits=6,decimal_places=2)	#borrar
	id_cat=models.ForeignKey(model_categoria)	
	def __unicode__(self):
	 	return "%s"%(self.nombre)

class model_reserva_producto(models.Model):
	id_Usuario=models.ForeignKey(model_producto)
	cantidad = models.IntegerField(unique=True)
	def __unicode__(self):
		return"%s Materia %s"%(self.id_Usuario.nombre)

class pedido(models.Model):
	cliente=models.ForeignKey(User)
	producto=models.ManyToManyField(model_producto)
	cantidad=models.IntegerField()
	precio_total=models.FloatField()
	fecha=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.producto

class carrito(models.Model):
	id_sesion=models.CharField(max_length=200)
	estado=models.BooleanField(default=False)
	producto=models.ForeignKey(model_producto)
	cantidad=models.IntegerField()
	

class compra(models.Model):
	idSession=models.CharField(max_length=200)
	id_pro=models.ForeignKey(model_producto)
	cantidad=models.DecimalField(max_digits=5,decimal_places=0)

class model_almacen (models.Model):	
	cant_entra=models.DecimalField(max_digits=6,decimal_places=2)	
	cant_sal=models.DecimalField(max_digits=6,decimal_places=2)		
	fecha=models.DateField()
	stock=models.IntegerField(unique=True)
	id_produc=models.ForeignKey(model_producto)
	id_prove=models.ForeignKey(model_proveedor)
	def __unicode__(self):
	 	return "%s"%(self.fecha)

class cliente (models.Model):
	nombre=models.CharField(max_length=200)
	apellidos=models.CharField(max_length=200)
	ci=models.IntegerField(unique=True)
	direccion=models.CharField(max_length=200)
	telefono=models.IntegerField()
	email=models.EmailField(max_length=75)
	zona=models.CharField(max_length=200)
	fecha=models.DateField(auto_now=True)
	def __unicode__(self):
		return "%s "%(self.nombre)

class Entrada (models.Model):
	titulo = models.CharField(max_length=100)
	contenido = models.TextField()
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.titulo
		
class Comentario (models.Model):
	fechacreacion = models.DateTimeField(auto_now_add=True)
	autor = models.CharField(max_length=100)
	mensaje = models.TextField()
	identrada = models.ForeignKey(Entrada)
	
	def __str__(self):
		return str("%s %s " % (self.identrada,self.mensaje[:60]))
# class Compra(models.Model):
# 	idSession=models.CharField(max_length=200)
# 	idPro=models.ForeignKey(model_producto)
# 	cantidad=models.DecimalField(max_digits=5,decimal_places=0)

class ubicacion (models.Model):
	nombre = models.CharField(max_length=200)
	lat =models.CharField(max_length=50)
	lng =models.CharField(max_length=50)
	fecha =models.DateTimeField(auto_now_add=True)
	user =models.ForeignKey(cliente)

	def __unicode__(self):
		return self.nombre

		
