from django.forms.models import model_to_dict
from geodesia.models import EquiposGeodesicos
from scripts.p1.utils import snap_geometry, geometry_is_valid
#point_inside_any_polygon


class EquiposGeodesicosCrud:

    def insert(self, d):
        try:
            geom = snap_geometry(d["geom"])

            if not geometry_is_valid(geom):
                return {"ok": False, "message": "Geometría inválida", "data": None}

            #inside = point_inside_any_polygon(geom)
            #if not inside:
                return {"ok": False, "message": "El punto está fuera de cualquier polígono de zonas_trabajo", "data": None}

            obj = EquiposGeodesicos(
                nombre_equipo=d["nombre_equipo"],
                tipo_equipo=d.get("tipo_equipo"),
                marca=d.get("marca"),
                modelo=d.get("modelo"),
                fecha_toma_datos=d["fecha_toma_datos"],
                ficha_tecnica=d.get("ficha_tecnica"),
                geom=geom
            )
            obj.save()

            return {"ok": True, "message": "Data inserted", "data": [{"id": obj.id}]}
        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def update(self, d):
        try:
            obj = EquiposGeodesicos.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False,"message": f"No existe el equipo con id {d['id']}","data": []}

            geom = snap_geometry(d["geom"])

            if not geometry_is_valid(geom):
                return {"ok": False, "message": "Geometría inválida", "data": None}

            #inside = point_inside_any_polygon(geom)
            #if not inside:
                return {"ok": False,"message": "El punto está fuera de cualquier polígono de zonas_trabajo","data": None}

            obj.nombre_equipo = d["nombre_equipo"]
            obj.tipo_equipo = d.get("tipo_equipo")
            obj.marca = d.get("marca")
            obj.modelo = d.get("modelo")
            obj.fecha_toma_datos = d["fecha_toma_datos"]
            obj.ficha_tecnica = d.get("ficha_tecnica")
            obj.geom = geom
            obj.save()

            return {"ok": True, "message": "Data updated", "data": [{"rows_updated": 1}]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def delete(self, d):
        try:
            obj = EquiposGeodesicos.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False,"message": f"No existe el equipo con id {d['id']}","data": []}

            obj.delete()
            return {"ok": True, "message": "Data deleted", "data": [{"rows_deleted": 1}]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def selectAsDicts(self, d):
        try:
            obj = EquiposGeodesicos.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False,"message": f"No existe el equipo con id {d['id']}","data": []}

            data = model_to_dict(obj)
            data["geom"] = obj.geom.wkt

            return {"ok": True, "message": "Data retrieved", "data": [data]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}

    def selectAsTuples(self, d):
        try:
            obj = EquiposGeodesicos.objects.filter(id=d["id"]).first()
            if not obj:
                return {"ok": False, "message": f"No existe el equipo con id {d['id']}", "data": []}

            tup = (
                obj.id,
                obj.nombre_equipo,
                obj.tipo_equipo,
                obj.marca,
                obj.modelo,
                obj.fecha_toma_datos,
                obj.ficha_tecnica,
                obj.geom.wkt,
            )

            return {"ok": True, "message": "Data retrieved", "data": [tup]}

        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}