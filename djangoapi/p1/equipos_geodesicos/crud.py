from p1.myLib.db import Db

class EquiposGeodesicosCrud:

    def insert(self, d):
        db = Db()
        try:
            sql_check = """
                SELECT ST_IsValid(g) AS valid
                FROM (
                    SELECT ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001) AS g
                ) t;
            """
            check = db.query(sql_check, [d["geom"]])[0]

            if not check["valid"]:
                return {"ok": False, "message": "Geometría inválida", "data": None}
###
            sql_within = """
                SELECT id
                FROM zonas_trabajo
                WHERE ST_Within(
                    ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001),
                    geom
                )
                LIMIT 1;
            """
            inside = db.query(sql_within, [d["geom"]])

            if not inside:
                return {
                    "ok": False,
                    "message": "El punto está fuera de cualquier polígono de zonas_trabajo",
                    "data": None
                }
###
            sql_insert = """
                INSERT INTO equipos_geodesicos
                (nombre_equipo, tipo_equipo, marca, modelo, fecha_toma_datos, ficha_tecnica, geom)
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001)
                )
                RETURNING id;
            """
            db.cur.execute(sql_insert, [
                d["nombre_equipo"],
                d.get("tipo_equipo"),
                d.get("marca"),
                d.get("modelo"),
                d["fecha_toma_datos"],
                d.get("ficha_tecnica"),
                d["geom"]
            ])
            new_id = db.cur.fetchone()["id"]
            db.conn.commit()

            return {"ok": True, "message": "Data inserted", "data": [{"id": new_id}]}

        except Exception as e:
            db.conn.rollback()
            return {"ok": False, "message": str(e), "data": None}
        finally:
            db.close()

    def update(self, d):
        db = Db()
        try:
            sql_check = """
                SELECT ST_IsValid(g) AS valid
                FROM (
                    SELECT ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001) AS g
                ) t;
            """
            check = db.query(sql_check, [d["geom"]])[0]

            if not check["valid"]:
                return {"ok": False, "message": "Geometría inválida", "data": None}
###
            sql_within = """
                SELECT id
                FROM zonas_trabajo
                WHERE ST_Within(
                    ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001),
                    geom
                )
                LIMIT 1;
            """
            inside = db.query(sql_within, [d["geom"]])

            if not inside:
                return {
                    "ok": False,
                    "message": "El punto está fuera de cualquier polígono de zonas_trabajo",
                    "data": None
                }
###
            sql_update = """
                UPDATE equipos_geodesicos
                SET nombre_equipo=%s,
                    tipo_equipo=%s,
                    marca=%s,
                    modelo=%s,
                    fecha_toma_datos=%s,
                    ficha_tecnica=%s,
                    geom=ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001)
                WHERE id=%s;
            """
            rows = db.execute(sql_update, [
                d["nombre_equipo"],
                d.get("tipo_equipo"),
                d.get("marca"),
                d.get("modelo"),
                d["fecha_toma_datos"],
                d.get("ficha_tecnica"),
                d["geom"],
                d["id"]
            ])

            return {"ok": True, "message": "Data updated", "data": [{"rows_updated": rows}]}

        except Exception as e:
            db.conn.rollback()
            return {"ok": False, "message": str(e), "data": None}
        finally:
            db.close()

    def delete(self, d):
        db = Db()
        try:
            rows = db.execute("DELETE FROM equipos_geodesicos WHERE id=%s;", [d["id"]])
            return {"ok": True, "message": "Data deleted", "data": [{"rows_deleted": rows}]}
        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}
        finally:
            db.close()

    def selectAsDicts(self, d):
        db = Db()
        try:
            sql = """
                SELECT
                    id, nombre_equipo, tipo_equipo, marca, modelo, fecha_toma_datos,
                    ficha_tecnica, ST_AsText(geom) AS geom
                FROM equipos_geodesicos
                WHERE id=%s;
            """
            data = db.query(sql, [d["id"]])
            return {"ok": True, "message": "Data retrieved", "data": data}
        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}
        finally:
            db.close()

    def selectAsTuples(self, d):
        db = Db(use_dict_rows=False)
        try:
            sql = """
                SELECT
                    id, nombre_equipo, tipo_equipo, marca, modelo, fecha_toma_datos,
                    ficha_tecnica, ST_AsText(geom) AS geom
                FROM equipos_geodesicos
                WHERE id=%s;
            """
            data = db.query(sql, [d["id"]])
            return {"ok": True, "message": "Data retrieved", "data": data}
        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}
        finally:
            db.close()