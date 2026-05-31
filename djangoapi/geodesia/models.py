# Create your models here.
#from django.db import models
#from django.contrib.gis.db import models as gis_models
#from django.contrib.gis.geos import GEOSGeometry

from django.db import models
from django.contrib.gis.db import models as gis_models

SRID_STORAGE = 4326
SRID_METRIC = 25830  # para calcular área, perímetro y longitud en metros


class ZonasTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField()
    responsable = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    area = models.FloatField(blank=True, null=True)
    perimetro = models.FloatField(blank=True, null=True)

    geom = gis_models.PolygonField(srid=SRID_STORAGE)

    class Meta:
        db_table = 'zonas_trabajo'

    def save(self, *args, **kwargs):
        if self.geom:
            g = self.geom.clone()
            g.transform(SRID_METRIC)
            self.area = g.area
            self.perimetro = g.length

        super().save(*args, **kwargs)


class RutasLevantamiento(models.Model):
    codigo_ruta = models.CharField(max_length=50)
    equipo_usado = models.CharField(max_length=100, blank=True, null=True)
    operador = models.CharField(max_length=100, blank=True, null=True)
    fecha_toma = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

    longitud = models.FloatField(blank=True, null=True)

    geom = gis_models.LineStringField(srid=SRID_STORAGE)

    class Meta:
        db_table = 'rutas_levantamiento'

    def save(self, *args, **kwargs):
        if self.geom:
            g = self.geom.clone()
            g.transform(SRID_METRIC)
            self.longitud = g.length

        super().save(*args, **kwargs)


class EquiposGeodesicos(models.Model):
    nombre_equipo = models.CharField(max_length=100)
    tipo_equipo = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    fecha_toma_datos = models.DateField()
    ficha_tecnica = models.TextField(blank=True, null=True)

    geom = gis_models.PointField(srid=SRID_STORAGE)

    class Meta:
        db_table = 'equipos_geodesicos'