from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

#SISTEMA DE REFERENCIA EN EL QUE ALMACENAREMOS LAS GEOMETRIAS DE LA BD
SRID_STORAGE = 4326
#REDONDEDO A 0.0001
SNAP = 0.0001
#SISTEMA DE COORDENADAS PROYECTADA PARA EL CALCULO DE AREA,PERIMETRO, LONGITUD - CASO ESPAÑA
SRID_METRIC = 25830

#DEF EN EL CUAL RECIBE LA GEOMETRIA, CONVIERTE A POSTGIS Y REDONDEA A LA PRECISION USANDO ST_SNAPTOGRID
def snap_geometry(wkt: str):
    with connection.cursor() as cur:
        cur.execute(
            """
            SELECT ST_AsText(ST_SnapToGrid(ST_GeomFromText(%s, %s),%s))""",
            [wkt, SRID_STORAGE, SNAP]
        )
        snapped_wkt = cur.fetchone()[0]

    return GEOSGeometry(snapped_wkt, srid=SRID_STORAGE)

#COMPROBACION SI LA GEOMETRIA ES VALIDA
def geometry_is_valid(geom):
    return geom.valid

#INTERSECCION DE POLIGONOS YA EXISTENTES EN LA CAPA DE ZONAS DE TRABAJO
def polygon_intersects_same_layer(geom, exclude_id=None):
    sql = """
        SELECT id
        FROM public.zonas_trabajo
        WHERE ST_Intersects(
            geom,
            ST_GeomFromText(%s, %s)
        )
    """
    params = [geom.wkt, SRID_STORAGE]

    if exclude_id is not None:
        sql += " AND id <> %s"
        params.append(exclude_id)

    with connection.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

    
#COMPRUEBA SI UNA LINEA INTERSECTA CON OTRA LIENA YA EXISTENTE EN LA CAPA RUTA_LEVANTAMIENTO
def line_intersects_same_layer(geom, exclude_id=None):
    sql = """
        SELECT id
        FROM public.rutas_levantamiento
        WHERE ST_Intersects(
            geom,
            ST_GeomFromText(%s, %s)
        )
    """
    params = [geom.wkt, SRID_STORAGE]

    if exclude_id is not None:
        sql += " AND id <> %s"
        params.append(exclude_id)

    with connection.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


#COMPRUEBA SI EL PUNTO ESTA DENTRO DE ALMENOS UN POLIGONO DE LA CAPA DE POLIGONO
def point_inside_any_polygon(geom):
    sql = """
        SELECT id
        FROM public.zonas_trabajo
        WHERE ST_Within(
            ST_GeomFromText(%s, %s),
            geom
        )
        LIMIT 1
    """
    with connection.cursor() as cur:
        cur.execute(sql, [geom.wkt, SRID_STORAGE])
        return cur.fetchone()