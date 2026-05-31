import sys

from p1.zonas_trabajo.crud import ZonasTrabajoCrud
from p1.rutas_levantamiento.crud import RutasLevantamientoCrud
from p1.equipos_geodesicos.crud import EquiposGeodesicosCrud

class MainGeodesiaOOP:

    def __init__(self):
        self.tables = {
            "zonastrabajo": ZonasTrabajoCrud(),
            "rutaslevantamiento": RutasLevantamientoCrud(),
            "equipogeodesico": EquiposGeodesicosCrud(),
        }

    def get_data(self, table_name, method_name):
        """
        Devuelve un diccionario de prueba según la tabla y el método.
        """

        if table_name == "zonastrabajo":
            if method_name == "insert":
                return {
                    "nombre": "Zona Norte",
                    "descripcion": "Área de trabajo geodésico en el sector norte",
                    "fecha_creacion": "2026-03-26",
                    "responsable": "Ana Pérez",
                    "estado": "activa",
                    "geom": "POLYGON((-0.3800 39.4700,-0.3790 39.4700,-0.3790 39.4710,-0.3800 39.4710,-0.3800 39.4700))"
                }
            elif method_name == "update":
                return {
                    "id": 1,
                    "nombre": "Zona Norte Actualizada",
                    "descripcion": "Área de trabajo corregida",
                    "fecha_creacion": "2026-03-26",
                    "responsable": "Ana Pérez",
                    "estado": "en_revision",
                    "geom": "POLYGON((-0.3800 39.4700,-0.3788 39.4700,-0.3788 39.4712,-0.3800 39.4712,-0.3800 39.4700))"
                }
            elif method_name in ["selectAsDicts", "selectAsTuples", "delete"]:
                return {"id": 1}

        elif table_name == "rutaslevantamiento":
            if method_name == "insert":
                return {
                    "codigo_ruta": "RUTA-001",
                    "equipo_usado": "GPS RTK",
                    "operador": "Carlos Ruiz",
                    "fecha_toma": "2026-03-26",
                    "observaciones": "Recorrido principal del sector",
                    "geom": "LINESTRING(-0.3799 39.4701,-0.3797 39.4704,-0.3795 39.4708)"
                }
            elif method_name == "update":
                return {
                    "id": 1,
                    "codigo_ruta": "RUTA-001-REV",
                    "equipo_usado": "GPS RTK Leica",
                    "operador": "Carlos Ruiz",
                    "fecha_toma": "2026-03-26",
                    "observaciones": "Ruta ajustada tras revisión",
                    "geom": "LINESTRING(-0.3799 39.4701,-0.3796 39.4705,-0.3793 39.4709)"
                }
            elif method_name in ["selectAsDicts", "selectAsTuples", "delete"]:
                return {"id": 1}

        elif table_name == "equipogeodesico":
            if method_name == "insert":
                return {
                    "nombre_equipo": "Equipo Leica 01",
                    "tipo_equipo": "Estacion total",
                    "marca": "Leica",
                    "modelo": "TS16",
                    "fecha_toma_datos": "2026-03-26",
                    "ficha_tecnica": "Equipo de alta precision",
                    "geom": "POINT(-0.3796 39.4705)"
                }
            elif method_name == "update":
                return {
                    "id": 1,
                    "nombre_equipo": "Equipo Leica 01 PRO",
                    "tipo_equipo": "Estacion total",
                    "marca": "Leica",
                    "modelo": "TS16 Plus",
                    "fecha_toma_datos": "2026-03-26",
                    "ficha_tecnica": "Equipo actualizado de alta precision",
                    "geom": "POINT(-0.3795 39.4706)"
                }
            elif method_name in ["selectAsDicts", "selectAsTuples", "delete"]:
                return {"id": 1}

        return None

    def run(self, table_name, method_name):
        if table_name not in self.tables:
            print({
                "ok": False,
                "message": f"Tabla no válida: {table_name}",
                "data": None
            })
            return

        crud_obj = self.tables[table_name]

        if not hasattr(crud_obj, method_name):
            print({
                "ok": False,
                "message": f"Método no válido: {method_name}",
                "data": None
            })
            return

        data = self.get_data(table_name, method_name)
        if data is None:
            print({
                "ok": False,
                "message": f"No hay datos de prueba para {table_name}.{method_name}",
                "data": None
            })
            return

        method = getattr(crud_obj, method_name)
        result = method(data)
        print(result)


def main():
    if len(sys.argv) != 3:
        print("Uso: python scripts/p1/main_geodesiaOOP.py <tabla> <metodo>")
        print("Tablas: zonastrabajo | rutaslevantamiento | equipogeodesico")
        print("Métodos: insert | update | delete | selectAsDicts | selectAsTuples")
        return

    table_name = sys.argv[1]
    method_name = sys.argv[2]

    app = MainGeodesiaOOP()
    app.run(table_name, method_name)


if __name__ == "__main__":
    main()