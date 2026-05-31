from django.forms.models import model_to_dict
from geodesia.models import ZonasTrabajo
from scripts.p1.utils import snap_geometry, geometry_is_valid, polygon_intersects_same_layer

#CRUD USANDO DJANGO MODELS
class ZonasTrabajoCrud:

    def insert(self, d):
        try:
            #REDONDEAR LA GEOMETRIA ANTES DE GUARDAR
            geom = snap_geometry(d["geom"])

            #VALIDAMOS LA GEOMETRIA
            if not geometry_is_valid(geom):
                return {"ok": False, "message": "Geometría inválida", "data": None}

            #RECHAZAR LOS POLIGONOS QUE SE INTERSECTAN
            inter = polygon_intersects_same_layer(geom)
            if inter:
                return {"ok": False, "message": "El polígono intersecta con otro polígono de la misma capa", "data": inter}


            obj = ZonasTrabajo(
                nombre=d["nombre"],
                descripcion=d.get("descripcion"),
                fecha_creacion=d["fecha_creacion"],
                responsable=d.get("responsable"),
                estado=d.get("estado"),
                geom=geom
            )
            obj.save()

            return {"ok": True, "message": "Data inserted", "data": [{"id": obj.id}]}
        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def update(self, d):
        try:
            obj = ZonasTrabajo.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False, "message": f"No existe la zona con id {d['id']}", "data": []}

            geom = snap_geometry(d["geom"])

            if not geometry_is_valid(geom):
                return {"ok": False, "message": "Geometría inválida", "data": None}

            inter = polygon_intersects_same_layer(geom, exclude_id=obj.id)
            if inter:
                return {"ok": False, "message": "El polígono intersecta con otro polígono de la misma capa", "data": [{"id": row[0]} for row in inter]}

            obj.nombre = d["nombre"]
            obj.descripcion = d.get("descripcion")
            obj.fecha_creacion = d["fecha_creacion"]
            obj.responsable = d.get("responsable")
            obj.estado = d.get("estado")
            obj.geom = geom
            obj.save()

            return {"ok": True, "message": "Data updated", "data": [{"rows_updated": 1}]}
        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def delete(self, d):
        try:
            #comprobar si existe el id
            obj = ZonasTrabajo.objects.filter(id=d["id"]).first()
            if not obj:
                return {
                    "ok": False,
                    "message": f"No existe la zona con id {d['id']}",
                    "data": [],
                }

            obj.delete()
            return {"ok": True, "message": "Data deleted", "data": [{"rows_deleted": 1}]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}
        
    def selectAsDicts(self, d):
        try:
            obj = ZonasTrabajo.objects.filter(id=d["id"]).first()
            if not obj:
                return {
                    "ok": False,
                    "message": f"No existe la zona con id {d['id']}",
                    "data": [],
                }

            data = model_to_dict(obj)
            data["geom"] = obj.geom.wkt

            return {"ok": True, "message": "Data retrieved", "data": [data]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}


    def selectAsTuples(self, d):
        try:
            obj = ZonasTrabajo.objects.filter(id=d["id"]).first()
            if not obj:
                return {
                    "ok": False,
                    "message": f"No existe la zona con id {d['id']}",
                    "data": [],
                }

            # construimos la tupla para que cumpla con el enunciado
            tup = (
                obj.id,
                obj.nombre,
                obj.descripcion,
                obj.fecha_creacion,
                obj.responsable,
                obj.estado,
                obj.area,
                obj.perimetro,
                obj.geom.wkt,
            )

            return {"ok": True, "message": "Data retrieved", "data": [tup]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}
        

#para realizar el select all
    def selectAll(self, d=None):
        try:
            objs = ZonasTrabajo.objects.all().order_by("id")

            data = []

            for obj in objs:
                item = model_to_dict(obj)
                item["geom"] = obj.geom.wkt if obj.geom else None
                data.append(item)

            return {
                "ok": True,
                "message": "Data retrieved",
                "data": data
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }