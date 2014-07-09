from django.conf.urls import patterns, include, url
from views import *

from django.conf import settings
urlpatterns = patterns('',
	 url(r'media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
	 url(r'^$',inicio),
	 #url(r'^regisusuario$',nuevoUsuario),
	 #url(r'^ingresar$',ingresar),
	 url(r'^home$',home),
	 url(r'^index$',index),
	 url(r'^logueo$',view_logueo),
	 url(r'^cerrar$',cerrar),
	 url(r'^regis_distri$',view_regis_distri),
	 url(r'^ver_distri$',view_ver_distri),
	 url(r'^regis_cate$',view_regis_cate),
	 url(r'^registro_proveedor$',view_regis_proveedor),
	 url(r'^regis_produc$',view_regis_produc),
	 url(r'^categoria/(?P<id>\d+)$', recuperar),
	 # url(r'^modificar/(?P<id>\d+)/$',modificarCliente),
	 url(r'^reservas$',reservar),
	 url(r'^productos$',productos),
	 url(r'^promocion$',Promocion),
	 url(r'^noticias$',noticias),
	 url(r'^acerca$',acerca),
	 url(r'^ver_producto$',view_ver_producto),
	 url(r'^ver_cate$',view_ver_cate),
	url(r'^addProducto$',add_product_view),
	url(r'^mostrar$',view_carrito),
	url(r'^mostrar$',compra),
	
	url(r'^listado$',main),
	url(r'^regis_entrada$',view_regiscomentario),
	#url(r'^edit/producto/(?P<id_prod>.*)/$', 'edit_product_view', name="vista_editar_producto"),
	 #url(r'^eliminar/(?P<id_client>\d+)/$',eliminar),

	 url(r'^entrada/(?P<pk>\d+)/$',entrada),
	url(r'^month/(\d+)/(\d+)/$',month),
	url(r'^poncomentario/(\d+)/$',poncomentario),
	

	url(r'^mapa$',mapa),
	url(r'^ss$',index3333),
    url(r'^coords/save$', coords_save),

#carrito de aqui

	    url(r'^productos/$',productos),
    url(r'^mostrar/carrito/$',carrito_mostrar),
    url(r'^cargar/carrito/(\d+)/$',cargar_carrito),
    url(r'^carrito/add/(\d+)/$',carrito_add),
    url(r'^carrito/eliminar/(?P<id>\d+)/$',eliminar_de_carrito),
    url(r'^producto/(?P<id>\d+)/$',listar_producto),
    url(r'^confirmar/compra/$',confirmar_compra),
    url(r'^producto/comprar/final/$',realizar_transaccion),
    url(r'^regiscliente$',home),
    
) 