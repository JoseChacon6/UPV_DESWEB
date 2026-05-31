from django.urls import path, include
from . import views

#esto es de django framework, no va, se encarga de registrar
#router = routers.DefaultRouter()
#router.register(r'buildings', views.BuildingsModelViewSet)
#router.register(r'owners', views.OwnersModelViewSet)
#router.register(r'buildingsowners', views.BuildingsOwnersModelViewSet)

#AQUI TENEMOS QUE CAMBIAR
#definimos las urls, cada una con su vista en el fichero views.py, y el nombre de la url
urlpatterns = [
    path("hello_geodesia/", views.HelloGeodesia.as_view(),name="hello_geodesia"),
    path("zonas_trabajo/", views.ZonasTrabajo.as_view(),name="zonas_trabajo"),
    path("zonas_trabajo_insert/", views.ZonasTrabajoInsert.as_view(),name="zonas_trabajo_insert"),
    path("zonas_trabajo_delete/", views.ZonasTrabajoDelete.as_view(),name="zonas_trabajo_delete"),

    #para zonas de trabajo
    path('ZonasTrabajo_view/<str:action>/', views.ZonasTrabajoView.as_view(), name='ZonasTrabajo_views'),  # POST requests
    path('ZonasTrabajo_view/<str:action>/<int:id>/', views.ZonasTrabajoView.as_view(), name='ZonasTrabajo_views'),  ##TENEMOS LA ACCION Y EL ID PARA LOS METODOS QUE LO NECESITEN COMO SELECTONE, DELETE
    #para rutas_levantamiento
    path('RutasLevantamiento_view/<str:action>/', views.RutasLevantamientoView.as_view(), name='RutasLevantamiento_views'),  # POST requests
    path('RutasLevantamiento_view/<str:action>/<int:id>/', views.RutasLevantamientoView.as_view(), name='RutasLevantamiento_views'), 

    #para equipos geodesicos
    path('EquiposGeodesicos_view/<str:action>/', views.EquiposGeodesicosView.as_view(), name='EquiposGeodesicos_views'),  # POST requests
    path('EquiposGeodesicos_view/<str:action>/<int:id>/', views.EquiposGeodesicosView.as_view(), name='EquiposGeodesicos_views'), 

]