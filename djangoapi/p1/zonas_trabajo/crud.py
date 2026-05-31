from p1.myLib.db import Db

class ZonasTrabajoCrud:

    def insert(self, d):
        db = Db()
        try:
            sql_check = """
                SELECT
                    ST_IsValid(g) AS valid,
                    ST_Area(ST_Transform(g, 25830)) AS area,
                    ST_Perimeter(ST_Transform(g, 25830)) AS perimetro
                FROM (
                    SELECT ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001) AS g
                ) t;
            """
            check = db.query(sql_check, [d["geom"]])[0]

            if not check["valid"]:
                return {"ok": False, "message": "Geometría inválida", "data": None}
###
            sql_inter = """
                SELECT id
                FROM zonas_trabajo
                WHERE ST_Intersects(
                    geom,
                    ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001)
                );
            """
            inter = db.query(sql_inter, [d["geom"]])

            if inter:
                return {
                    "ok": False,
                    "message": "El polígono intersecta con otro polígono de la misma capa",
                    "data": inter
                }
###
            sql_insert = """
                INSERT INTO zonas_trabajo
                (nombre, descripcion, fecha_creacion, responsable, estado, area, perimetro, geom)
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001)
                )
                RETURNING id;
            """
            db.cur.execute(sql_insert, [
                d["nombre"],
                d.get("descripcion"),
                d["fecha_creacion"],
                d.get("responsable"),
                d.get("estado"),
                check["area"],
                check["perimetro"],
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
                SELECT
                    ST_IsValid(g) AS valid,
                    ST_Area(ST_Transform(g, 25830)) AS area,
                    ST_Perimeter(ST_Transform(g, 25830)) AS perimetro
                FROM (
                    SELECT ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001) AS g
                ) t;
            """
            check = db.query(sql_check, [d["geom"]])[0]

            if not check["valid"]:
                return {"ok": False, "message": "Geometría inválida", "data": None}

            sql_inter = """
                SELECT id
                FROM zonas_trabajo
                WHERE id <> %s
                  AND ST_Intersects(
                    geom,
                    ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001)
                  );
            """
            inter = db.query(sql_inter, [d["id"], d["geom"]])

            if inter:
                return {
                    "ok": False,
                    "message": "El polígono intersecta con otro polígono de la misma capa",
                    "data": inter
                }

            sql_update = """
                UPDATE zonas_trabajo
                SET nombre=%s,
                    descripcion=%s,
                    fecha_creacion=%s,
                    responsable=%s,
                    estado=%s,
                    area=%s,
                    perimetro=%s,
                    geom=ST_SnapToGrid(ST_GeomFromText(%s, 4326), 0.0001)
                WHERE id=%s;
            """
            rows = db.execute(sql_update, [
                d["nombre"],
                d.get("descripcion"),
                d["fecha_creacion"],
                d.get("responsable"),
                d.get("estado"),
                check["area"],
                check["perimetro"],
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
            rows = db.execute("DELETE FROM zonas_trabajo WHERE id=%s;", [d["id"]])
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
                    id, nombre, descripcion, fecha_creacion, responsable, estado,
                    area, perimetro,
                    ST_AsText(geom) AS geom
                FROM zonas_trabajo
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
                    id, nombre, descripcion, fecha_creacion, responsable, estado,
                    area, perimetro,
                    ST_AsText(geom) AS geom
                FROM zonas_trabajo
                WHERE id=%s;
            """
            data = db.query(sql, [d["id"]])
            return {"ok": True, "message": "Data retrieved", "data": data}
        except Exception as e:
            return {"ok": False, "message": str(e), "data": None}
        finally:
            db.close()