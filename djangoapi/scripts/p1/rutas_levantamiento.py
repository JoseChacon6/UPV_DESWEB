from django.forms.models import model_to_dict
from geodesia.models import RutasLevantamiento
from scripts.p1.utils import snap_geometry, geometry_is_valid, line_intersects_same_layer

#CRUD PARA LA TABLA RUTAS DE LEVANTAMIENTO
class RutasLevantamientoCrud:

    def insert(self, d):
        try:
            geom = snap_geometry(d["geom"])

            if not geometry_is_valid(geom):
                return {"ok": False, "message": "Geometría inválida", "data": None}

            #RECHAZAR LINEAS QUE SE INTERSECTAN CON OTRAS
            inter = line_intersects_same_layer(geom)
            if inter:
                return {"ok": False,"message": "La línea intersecta con otra línea de la misma capa","data": [{"id": row[0]} for row in inter]}

            obj = RutasLevantamiento(
                codigo_ruta=d["codigo_ruta"],
                equipo_usado=d.get("equipo_usado"),
                operador=d.get("operador"),
                fecha_toma=d["fecha_toma"],
                observaciones=d.get("observaciones"),
                geom=geom,
            )
            obj.save()

            return {"ok": True, "message": "Data inserted", "data": [{"id": obj.id}]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def update(self, d):
        try:
            obj = RutasLevantamiento.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False,"message": f"No existe la ruta con id {d['id']}","data": []}

            geom = snap_geometry(d["geom"])

            if not geometry_is_valid(geom):
                return {"ok": False, "message": "Geometría inválida", "data": None}

            inter = line_intersects_same_layer(geom, exclude_id=obj.id)
            if inter:
                return {"ok": False, "message": "La línea intersecta con otra línea de la misma capa","data": [{"id": row[0]} for row in inter]}

            obj.codigo_ruta = d["codigo_ruta"]
            obj.equipo_usado = d.get("equipo_usado")
            obj.operador = d.get("operador")
            obj.fecha_toma = d["fecha_toma"]
            obj.observaciones = d.get("observaciones")
            obj.geom = geom
            obj.save()

            return {"ok": True, "message": "Data updated", "data": [{"rows_updated": 1}]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def delete(self, d):
        try:
            obj = RutasLevantamiento.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False, "message": f"No existe la ruta con id {d['id']}","data": []}

            obj.delete()
            return {"ok": True, "message": "Data deleted", "data": [{"rows_deleted": 1}]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def selectAsDicts(self, d):
        try:
            obj = RutasLevantamiento.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False,"message": f"No existe la ruta con id {d['id']}","data": []}

            data = model_to_dict(obj)
            data["geom"] = obj.geom.wkt

            return {"ok": True, "message": "Data retrieved", "data": [data]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def selectAsTuples(self, d):
        try:
            obj = RutasLevantamiento.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False, "message": f"No existe la ruta con id {d['id']}", "data": []}

            tup = (
                obj.id,
                obj.codigo_ruta,
                obj.equipo_usado,
                obj.operador,
                obj.fecha_toma,
                obj.observaciones,
                obj.longitud,
                obj.geom.wkt,
            )

            return {"ok": True, "message": "Data retrieved", "data": [tup]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}