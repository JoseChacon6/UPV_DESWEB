import json

from scripts.p1.zonas_trabajo import ZonasTrabajoCrud
from scripts.p1.rutas_levantamiento import RutasLevantamientoCrud
from scripts.p1.equipos_geodesicos import EquiposGeodesicosCrud


def run(*args):
    """
    Uso general:
    python manage.py runscript scripts.p1.main_django_p1 --script-args <tabla> <operacion> [json]

    Tablas:
    - zonas_trabajo
    - rutas_levantamiento
    - equipos_geodesicos

    Operaciones:
    - insert
    - update
    - delete
    - selectAsDicts
    - selectAsTuples
    """

    if len(args) < 2:
        print({
            "ok": False,
            "message": "Uso: python manage.py runscript scripts.p1.main_django_p1 --script-args <tabla> <operacion> [json]",
            "data": None
        })
        return

    tabla = args[0]
    operacion = args[1]

    clases = {
        "zonas_trabajo": ZonasTrabajoCrud(),
        "rutas_levantamiento": RutasLevantamientoCrud(),
        "equipos_geodesicos": EquiposGeodesicosCrud(),
    }

    if tabla not in clases:
        print({
            "ok": False,
            "message": f"Tabla no válida: {tabla}",
            "data": None
        })
        return

    datos_demo = {
        "zonas_trabajo": {
            "nombre": "Zona Norte",
            "descripcion": "Polígono de trabajo norte",
            "fecha_creacion": "2026-03-25",
            "responsable": "Ana Pérez",
            "estado": "activa",
            "geom": "POLYGON((-0.3800 39.4700,-0.3790 39.4700,-0.3790 39.4710,-0.3800 39.4710,-0.3800 39.4700))"
        },
        "rutas_levantamiento": {
            "codigo_ruta": "RUTA-001",
            "equipo_usado": "GPS RTK",
            "operador": "Luis Gómez",
            "fecha_toma": "2026-03-25",
            "observaciones": "Ruta inicial",
            "geom": "LINESTRING(-0.3799 39.4701,-0.3797 39.4704,-0.3795 39.4708)"
        },
        "equipos_geodesicos": {
            "nombre_equipo": "Equipo 1",
            "tipo_equipo": "Estación total",
            "marca": "Leica",
            "modelo": "TS16",
            "fecha_toma_datos": "2026-03-25",
            "ficha_tecnica": "Equipo de alta precisión",
            "geom": "POINT(-0.3796 39.4705)"
        }
    }

    if len(args) >= 3:
        try:
            d = json.loads(args[2])
        except json.JSONDecodeError as e:
            print({
                "ok": False,
                "message": f"JSON inválido: {str(e)}",
                "data": None
            })
            return
    else:
        d = datos_demo[tabla]

    obj = clases[tabla]

    try:
        if operacion == "insert":
            print(obj.insert(d))

        elif operacion == "update":
            if "id" not in d:
                print({"ok": False, "message": "Para update debes enviar id", "data": None})
                return
            print(obj.update(d))

        elif operacion == "delete":
            if "id" not in d:
                print({"ok": False, "message": "Para delete debes enviar id", "data": None})
                return
            print(obj.delete({"id": d["id"]}))

        elif operacion == "selectAsDicts":
            if "id" not in d:
                print({"ok": False, "message": "Para selectAsDicts debes enviar id", "data": None})
                return
            print(obj.selectAsDicts({"id": d["id"]}))

        elif operacion == "selectAsTuples":
            if "id" not in d:
                print({"ok": False, "message": "Para selectAsTuples debes enviar id", "data": None})
                return
            print(obj.selectAsTuples({"id": d["id"]}))

        else:
            print({
                "ok": False,
                "message": f"Operación no válida: {operacion}",
                "data": None
            })

    except Exception as e:
        print({
            "ok": False,
            "message": str(e),
            "data": None
        })