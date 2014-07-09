from django.conf.urls import patterns, include, url
from apps.principal import views
from django.contrib import admin

from django.conf import settings
from django.contrib.auth.views import login
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hotel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('CocaPotosi.apps.principal.urls')),

    #RESERVAS
	url(r'^reserva/productos/select/$', 'reserva.views.productos'),
	url(r'^reserva/clientes/select/$', 'reserva.views.clientes'),
	url(r'^reserva/create/(?P<cliente_id>\d+)/$', 'reserva.views.create_reserva'),
	url(r'^reservas/seleccion/producto/(?P<reserva_id>\d+)/$', 'reserva.views.select_productos'),
	url(r'^reserva/producto/cantidad/(?P<reserva_id>\d+)/(?P<producto_id>\d+)/$', 'reserva.views.cantidad'),

	#Reporte
	url(r'^productos/pdf/$', 'reserva.views.productos_reporte'),
	url(r'^reserva/pdf/$', 'reserva.views.reserva_reporte'),
	url(r'^almacen/pdf/$', 'reserva.views.almacen_reporte'),
	url(r'^detalle/pdf/$', 'reserva.views.detalle_reporte'),
)
