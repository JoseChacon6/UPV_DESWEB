import sys
import json

from p1.zonas_trabajo.crud import ZonasTrabajoCrud
from p1.rutas_levantamiento.crud import RutasLevantamientoCrud
from p1.equipos_geodesicos.crud import EquiposGeodesicosCrud

TABLES = {
    "zonas_trabajo": ZonasTrabajoCrud(),
    "rutas_levantamiento": RutasLevantamientoCrud(),
    "equipos_geodesicos": EquiposGeodesicosCrud(),
}

METHODS = {
    "insert",
    "update",
    "delete",
    "selectAsDicts",
    "selectAsTuples",
}

def main():
    if len(sys.argv) != 4:
        print("esta mal la escritura del codigo")
        return

    table_name = sys.argv[1]
    method_name = sys.argv[2]
    payload_text = sys.argv[3]

    if table_name not in TABLES:
        print({"ok": False, "message": f"Tabla no válida: {table_name}", "data": None})
        return

    if method_name not in METHODS:
        print({"ok": False, "message": f"Método no válido: {method_name}", "data": None})
        return

    try:
        payload = json.loads(payload_text)
    except Exception as e:
        print({"ok": False, "message": f"JSON inválido: {str(e)}", "data": None})
        return

    obj = TABLES[table_name]
    method = getattr(obj, method_name)
    result = method(payload)
    print(result)


if __name__ == "__main__":
    main()