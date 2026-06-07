import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy import text

from core.utils import sanitize_for_json

from .base import BaseRepository

logger = logging.getLogger("repo-inventory")

class InventoryRepository(BaseRepository):
    """Repositorio para el dominio de Movimientos de Inventario y Consumos."""

    def get_consumos_ceco(self, ceco: str) -> dict:
        ceco_clean = ceco.strip().upper()
        try:
            # Consulta Histórica (con dedup)
            query_hist = """
                SELECT
                    material,
                    MAX(texto_breve_material) as descripcion,
                    MAX(umb) as umb,
                    SUM(cantidad) * -1 as cantidad_total,
                    SUM(importe_ml) * -1 as costo_total,
                    (
                        SELECT ABS(importe_ml / cantidad)
                        FROM inventory_movements i2
                        WHERE UPPER(TRIM(i2.material)) = UPPER(TRIM(inventory_movements.material))
                          AND i2.cantidad != 0
                          AND i2.cmv = '201'
                        ORDER BY substr(i2.fe_contab, 7, 4) || '-' || substr(i2.fe_contab, 4, 2) || '-' || substr(i2.fe_contab, 1, 2) DESC, i2.hora DESC
                        LIMIT 1
                    ) as precio_unitario
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(ce_coste)) = :ceco
                  AND fe_contab LIKE :year
                GROUP BY material
                ORDER BY costo_total DESC
            """
            current_year_str = str(datetime.now().year)
            df_hist = pd.read_sql(text(query_hist), self.session.connection(), params={"ceco": ceco_clean, "year": f"%{current_year_str}"})
            df_hist = df_hist.astype(object).where(pd.notnull(df_hist), None)

            # Consulta Mes Actual (con dedup)
            current_month_str = datetime.now().strftime('%m-%Y')
            query_mes = """
                SELECT
                    material,
                    MAX(texto_breve_material) as descripcion,
                    MAX(umb) as umb,
                    SUM(cantidad) * -1 as cantidad_total,
                    SUM(importe_ml) * -1 as costo_total,
                    (
                        SELECT ABS(importe_ml / cantidad)
                        FROM inventory_movements i2
                        WHERE UPPER(TRIM(i2.material)) = UPPER(TRIM(inventory_movements.material))
                          AND i2.cantidad != 0
                          AND i2.cmv = '201'
                        ORDER BY substr(i2.fe_contab, 7, 4) || '-' || substr(i2.fe_contab, 4, 2) || '-' || substr(i2.fe_contab, 1, 2) DESC, i2.hora DESC
                        LIMIT 1
                    ) as precio_unitario
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(ce_coste)) = :ceco
                  AND fe_contab LIKE :month
                GROUP BY material
                ORDER BY costo_total DESC
            """
            df_mes = pd.read_sql(text(query_mes), self.session.connection(), params={"ceco": ceco_clean, "month": f"%{current_month_str}"})
            df_mes = df_mes.astype(object).where(pd.notnull(df_mes), None)

            return {
                "historico": df_hist.to_dict(orient="records"),
                "mes_actual": df_mes.to_dict(orient="records")
            }
        except Exception as e:
            logger.error(f"Error fetching consumos for CeCo {ceco}: {e}")
            raise

    def get_consumos_materiales(self, materiales: list) -> dict:
        mats_clean = [m.strip().upper() for m in materiales if m.strip()]
        if not mats_clean:
            return {"data": []}

        try:
            placeholders = ",".join([f":m{i}" for i in range(len(mats_clean))])
            params = {f"m{i}": m for i, m in enumerate(mats_clean)}

            current_month_str = datetime.now().strftime('%m-%Y')
            current_year_str = str(datetime.now().year)

            query = f"""
                SELECT
                    material,
                    MAX(texto_breve_material) as descripcion,
                    MAX(umb) as umb,
                    COALESCE((SELECT MAX(area_negocio)
                     FROM outbound_deliveries o
                     WHERE UPPER(TRIM(o.centro_costo)) = UPPER(TRIM(inventory_movements.ce_coste))
                       AND o.area_negocio IS NOT NULL
                       AND TRIM(o.area_negocio) != ''), 'SIN AREA') as area_negocio,
                    SUM(CASE WHEN fe_contab LIKE :month THEN cantidad ELSE 0 END) * -1 as cantidad_mes,
                    SUM(CASE WHEN fe_contab LIKE :month THEN importe_ml ELSE 0 END) * -1 as costo_mes,
                    SUM(cantidad) * -1 as cantidad_total,
                    SUM(importe_ml) * -1 as costo_total,
                    (
                        SELECT ABS(importe_ml / cantidad)
                        FROM inventory_movements i2
                        WHERE UPPER(TRIM(i2.material)) = UPPER(TRIM(inventory_movements.material))
                          AND i2.cantidad != 0
                          AND i2.cmv = '201'
                        ORDER BY substr(i2.fe_contab, 7, 4) || '-' || substr(i2.fe_contab, 4, 2) || '-' || substr(i2.fe_contab, 1, 2) DESC, i2.hora DESC
                        LIMIT 1
                    ) as precio_unitario
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(material)) IN ({placeholders})
                  AND fe_contab LIKE :year
                GROUP BY material, area_negocio
                ORDER BY material ASC, costo_total DESC
            """
            params["month"] = f"%{current_month_str}"
            params["year"] = f"%{current_year_str}"
            df = pd.read_sql(text(query), self.session.connection(), params=params)
            df = df.astype(object).where(pd.notnull(df), None)

            return {"data": df.to_dict(orient="records")}
        except Exception as e:
            logger.error(f"Error fetching consumos for Materiales: {e}")
            raise

    def get_material_trend(self, material: str, area_negocio: str, ceco: str) -> dict:
        material_clean = material.strip().upper()
        area_clean = area_negocio.strip()

        try:
            ceco_clean = ceco.strip().upper() if ceco else ""
            if ceco_clean:
                area_filter_sql = "UPPER(TRIM(ce_coste)) = :ceco"
                area_param = {"ceco": ceco_clean}
            else:
                area_filter_sql = """COALESCE((
                    SELECT MAX(area_negocio)
                    FROM outbound_deliveries o
                    WHERE UPPER(TRIM(o.centro_costo)) = UPPER(TRIM(inventory_movements.ce_coste))
                      AND o.area_negocio IS NOT NULL
                      AND TRIM(o.area_negocio) != ''
                ), 'SIN AREA') = :area"""
                area_param = {"area": area_clean}

            current_year = str(datetime.now().year)

            query = f"""
                SELECT
                    substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) as mes_orden,
                    substr(fe_contab, 4, 2) || '/' || substr(fe_contab, 7, 4) as mes_label,
                    SUM(cantidad) * -1 as cantidad,
                    SUM(importe_ml) * -1 as costo
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(material)) = :material
                  AND fe_contab LIKE :year
                  AND {area_filter_sql}
                GROUP BY mes_orden, mes_label
                ORDER BY mes_orden ASC
            """
            params = {"material": material_clean, "year": f"%{current_year}", **area_param}
            df = pd.read_sql(text(query), self.session.connection(), params=params)
            df = df.astype(object).where(pd.notnull(df), None)

            price_query = """
                SELECT (importe_ml / cantidad) as precio_unitario
                FROM inventory_movements
                WHERE UPPER(TRIM(material)) = :material
                  AND cantidad != 0
                  AND cmv = '201'
                ORDER BY substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2) DESC, hora DESC
                LIMIT 1
            """
            precio_unitario_row = self.session.connection().execute(text(price_query), {"material": material_clean}).fetchone()
            precio_unitario = abs(float(precio_unitario_row[0])) if precio_unitario_row and precio_unitario_row[0] is not None else 0

            return {
                "material": material,
                "area_negocio": area_negocio,
                "precio_unitario": precio_unitario,
                "current_year": current_year,
                "labels": df["mes_label"].tolist(),
                "cantidad": [float(v) if v is not None else 0 for v in df["cantidad"].tolist()],
                "costo": [float(v) if v is not None else 0 for v in df["costo"].tolist()]
            }
        except Exception as e:
            logger.error(f"Error fetching trend for material {material}: {e}")
            raise

    def check_table_exists(self) -> bool:
        try:
            res = self.session.execute(text("SELECT 1 FROM sqlite_master WHERE type='table' AND name='inventory_movements'")).scalar()
            return bool(res)
        except Exception:
            return False

    def get_cmv_summary(self, cmv_type: str, plan_type: str, year: Optional[str] = None) -> list:
        try:
            if cmv_type == "201":
                if plan_type.lower() == "planificado":
                    plan_filter = '''(
                        (inventory_movements.referencia GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR inventory_movements.referencia GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                        inventory_movements.texto_cab_documento GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR inventory_movements.texto_cab_documento GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
                    )'''
                else:
                    plan_filter = '''NOT (
                        (COALESCE(inventory_movements.referencia, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.referencia, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                        COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
                    ) AND
                    COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%cierre%' AND
                    COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%dev%' AND
                    COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%mes%' AND
                    COALESCE(inventory_movements.referencia, '') NOT LIKE '%cierre%' AND
                    COALESCE(inventory_movements.referencia, '') NOT LIKE '%dev%' AND
                    COALESCE(inventory_movements.referencia, '') NOT LIKE '%mes%'
                    '''
                area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(inventory_movements.ce_coste, 1, 6)), 'Mantencion')"
            elif cmv_type == "261":
                if plan_type.lower() == "planificado":
                    plan_filter = '''(
                        (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                        OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*'
                        OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
                    ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''
                else:
                    plan_filter = '''NOT (
                        (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                        OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*'
                        OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
                    ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''
                area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(inventory_movements.ceco_resp, ''), NULLIF(inventory_movements.ce_coste, '')), 1, 6)), 'Mantencion')"
            else:
                return []

            sql = f"""
            SELECT
                {area_expr} AS area_negocio,
                substr(inventory_movements.fe_contab, 7, 4) || '-' || substr(inventory_movements.fe_contab, 4, 2) AS mes,
                COUNT(inventory_movements.material) AS cantidad
            FROM inventory_movements
            WHERE inventory_movements.cmv = :cmv_type
              AND {plan_filter}
            """

            params = {"cmv_type": cmv_type}
            if year:
                sql += " AND inventory_movements.fe_contab LIKE :year"
                params["year"] = f"%{year}%"

            sql += """
            GROUP BY 1, 2
            ORDER BY 1, 2
            """

            df = pd.read_sql(text(sql), self.session.connection(), params=params)

            if df.empty:
                return []

            return sanitize_for_json(df)

        except Exception as e:
            logger.error(f"Error fetching cmv {cmv_type} summary: {e}")
            raise

    def get_cmv_area_details(self, cmv_type: str, plan_type: str, area: str, mes: Optional[str] = None, year: Optional[str] = None) -> list:
        try:
            if cmv_type == "201":
                if plan_type.lower() == "planificado":
                    plan_filter = '''(
                        (COALESCE(inventory_movements.referencia, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.referencia, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                        COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
                    )'''
                else:
                    plan_filter = '''NOT (
                        (COALESCE(inventory_movements.referencia, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.referencia, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                        COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
                    ) AND
                    COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%cierre%' AND
                    COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%dev%' AND
                    COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%mes%' AND
                    COALESCE(inventory_movements.referencia, '') NOT LIKE '%cierre%' AND
                    COALESCE(inventory_movements.referencia, '') NOT LIKE '%dev%' AND
                    COALESCE(inventory_movements.referencia, '') NOT LIKE '%mes%'
                    '''
                area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(inventory_movements.ce_coste, 1, 6)), 'Mantencion')"
            elif cmv_type == "261":
                if plan_type.lower() == "planificado":
                    plan_filter = '''(
                        (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                        OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*'
                        OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
                    ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''
                else:
                    plan_filter = '''NOT (
                        (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                        OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*'
                        OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
                    ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''
                area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(inventory_movements.ceco_resp, ''), NULLIF(inventory_movements.ce_coste, '')), 1, 6)), 'Mantencion')"
            else:
                return []

            sql = f"""
            SELECT
                inventory_movements.material,
                inventory_movements.texto_breve_material,
                COUNT(*) AS frecuencia,
                ROUND(AVG(inventory_movements.cantidad * -1), 2) AS promedio_retiro,
                ROUND(30.0 / COUNT(*), 1) AS dias_frecuencia
            FROM inventory_movements
            WHERE inventory_movements.cmv = :cmv_type
              AND {plan_filter}
            """

            params = {"cmv_type": cmv_type}
            if area:
                sql += f" AND {area_expr} = :area"
                params["area"] = area

            if mes:
                sql += " AND (substr(inventory_movements.fe_contab, 7, 4) || '-' || substr(inventory_movements.fe_contab, 4, 2)) = :mes"
                params["mes"] = mes
            elif year:
                sql += " AND inventory_movements.fe_contab LIKE :year"
                params["year"] = f"%{year}%"

            sql += """
            GROUP BY inventory_movements.material, inventory_movements.texto_breve_material
            ORDER BY frecuencia DESC
            """

            df = pd.read_sql(text(sql), self.session.connection(), params=params)

            if df.empty:
                return []

            return sanitize_for_json(df)

        except Exception as e:
            logger.error(f"Error fetching cmv {cmv_type} area details: {e}")
            raise

    def get_replenishment_suggestions(self, freq: str) -> dict:
        try:
            freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 12.0" # Default
            if freq == "1":
                freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 1.0"
            elif freq == "3":
                freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros > 1.0 AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 3.0"
            elif freq == "6":
                freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros > 3.0 AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 6.0"
            elif freq == "12":
                freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros > 6.0 AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 12.0"

            sql = f"""
            WITH MonthCount AS (
                SELECT CAST(COUNT(DISTINCT substr(fe_contab, 4, 7)) AS REAL) AS m_count
                FROM inventory_movements
                WHERE alm = '0060'
            ),
            Consumption AS (
                SELECT
                    TRIM(material) AS material,
                    MAX(texto_breve_material) AS descripcion,
                    MAX(umb) AS umb,
                    SUM(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN ABS(cantidad) ELSE 0 END) AS consumo_total,
                    COUNT(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN 1 END) AS n_retiros
                FROM inventory_movements
                WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
                GROUP BY TRIM(material)
            ),
            TotalBalance AS (
                SELECT
                    TRIM(material) AS material,
                    SUM(cantidad) AS balance
                FROM inventory_movements
                WHERE alm = '0060'
                GROUP BY TRIM(material)
            )
            SELECT
                c.material,
                c.descripcion,
                COALESCE(c.umb, i.umb) AS umb,
                COALESCE(i.stock_inicial, 0) AS stock_inicial,
                ROUND(COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0), 2) AS stock_actual,
                ROUND(c.consumo_total / (SELECT m_count FROM MonthCount), 2) AS consumo_mensual,
                CASE WHEN c.n_retiros > 0 THEN ROUND((SELECT m_count FROM MonthCount) / c.n_retiros, 2) ELSE 0 END AS frec_meses,
                CASE WHEN c.n_retiros > 0 THEN ROUND(c.consumo_total / c.n_retiros, 2) ELSE 0 END AS prom_retiro,
                ROUND((COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0), 2) AS autonomia_meses,
                CASE
                    WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 5.0 THEN 'A'
                    WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 1.0 THEN 'B'
                    ELSE 'C'
                END AS clasificacion_abc
            FROM Consumption c
            LEFT JOIN TotalBalance b ON c.material = b.material
            LEFT JOIN mb5b_initial_stock i ON c.material = TRIM(i.material)
            WHERE c.consumo_total > 0
              AND (COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0) < 1.0
              AND NOT (UPPER(COALESCE(c.umb, i.umb)) IN ('KG', 'GLN') AND (c.consumo_total / (SELECT m_count FROM MonthCount)) > 300)
              {freq_filter}
            ORDER BY autonomia_meses ASC, consumo_mensual DESC
            LIMIT 100;
            """

            result = self.session.execute(text(sql)).mappings().fetchall()
            data = [dict(row) for row in result]
            return {"data": data}
        except Exception as e:
            logger.error(f"Error fetching replenishment suggestions: {e}")
            raise

    def get_replenishment_export_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        try:
            sql = """
            WITH MonthCount AS (
                SELECT CAST(COUNT(DISTINCT substr(fe_contab, 4, 7)) AS REAL) AS m_count
                FROM inventory_movements
                WHERE alm = '0060'
            ),
            Consumption AS (
                SELECT
                    TRIM(material) AS material,
                    MAX(texto_breve_material) AS descripcion,
                    MAX(umb) AS umb,
                    SUM(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN ABS(cantidad) ELSE 0 END) AS consumo_total,
                    COUNT(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN 1 END) AS n_retiros
                FROM inventory_movements
                WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
                GROUP BY TRIM(material)
            ),
            TotalBalance AS (
                SELECT
                    TRIM(material) AS material,
                    SUM(cantidad) AS balance
                FROM inventory_movements
                WHERE alm = '0060'
                GROUP BY TRIM(material)
            )
            SELECT
                c.material AS "Material",
                c.descripcion AS "Descripción",
                COALESCE(c.umb, i.umb) AS "UMB",
                COALESCE(i.stock_inicial, 0) AS "Stock Inicial MB5B",
                ROUND(COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0), 2) AS "Stock Actual Calculado",
                ROUND(c.consumo_total / (SELECT m_count FROM MonthCount), 2) AS "Consumo Promedio Mensual",
                CASE WHEN c.n_retiros > 0 THEN ROUND((SELECT m_count FROM MonthCount) / c.n_retiros, 2) ELSE 0 END AS "Frecuencia de Retiro (Meses)",
                CASE WHEN c.n_retiros > 0 THEN ROUND(c.consumo_total / c.n_retiros, 2) ELSE 0 END AS "Promedio por Retiro",
                ROUND((COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0), 2) AS "Autonomía Global (Meses)",
                CASE
                    WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 5.0 THEN 'A'
                    WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 1.0 THEN 'B'
                    ELSE 'C'
                END AS "Clasificación ABC"
            FROM Consumption c
            LEFT JOIN TotalBalance b ON c.material = b.material
            LEFT JOIN mb5b_initial_stock i ON c.material = TRIM(i.material)
            WHERE c.consumo_total > 0
              AND (COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0) < 1.0
              AND NOT (UPPER(COALESCE(c.umb, i.umb)) IN ('KG', 'GLN') AND (c.consumo_total / (SELECT m_count FROM MonthCount)) > 300)
            ORDER BY "Autonomía Global (Meses)" ASC, "Consumo Promedio Mensual" DESC;
            """

            sql_areas = """
            WITH MonthCount AS (
                SELECT CAST(COUNT(DISTINCT substr(fe_contab, 4, 7)) AS REAL) AS m_count
                FROM inventory_movements
                WHERE alm = '0060'
            ),
            AreaMapping AS (
                SELECT
                    TRIM(material) AS material,
                    MAX(texto_breve_material) AS descripcion,
                    CASE
                        WHEN cmv = '261' THEN COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(ceco_resp, 1, 6)), 'Mantencion')
                        WHEN cmv IN ('201', '221') THEN COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(ce_coste, 1, 6)), 'Mantencion')
                        ELSE 'Otros'
                    END AS area_negocio,
                    SUM(ABS(cantidad)) AS area_consumo_total,
                    COUNT(1) AS area_n_retiros
                FROM inventory_movements
                WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
                GROUP BY TRIM(material), area_negocio
            ),
            TotalBalance AS (
                SELECT TRIM(material) AS material, SUM(cantidad) AS balance
                FROM inventory_movements WHERE alm = '0060' GROUP BY TRIM(material)
            ),
            GlobalConsumption AS (
                SELECT
                    TRIM(material) AS material,
                    SUM(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN ABS(cantidad) ELSE 0 END) AS global_consumo_total,
                    COUNT(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN 1 END) AS global_n_retiros
                FROM inventory_movements
                WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
                GROUP BY TRIM(material)
            )
            SELECT
                a.area_negocio AS "Área de Negocio",
                a.material AS "Material",
                a.descripcion AS "Descripción",
                COALESCE(i.umb, '') AS "UMB",
                ROUND(COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0), 2) AS "Stock Global Actual",
                ROUND(a.area_consumo_total / (SELECT m_count FROM MonthCount), 2) AS "Consumo Local (Mes)",
                CASE WHEN a.area_n_retiros > 0 THEN ROUND((SELECT m_count FROM MonthCount) / a.area_n_retiros, 2) ELSE 0 END AS "Frecuencia Local (Meses)",
                CASE WHEN a.area_n_retiros > 0 THEN ROUND(a.area_consumo_total / a.area_n_retiros, 2) ELSE 0 END AS "Promedio Retiro Local",
                ROUND((COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(a.area_consumo_total / (SELECT m_count FROM MonthCount), 0), 2) AS "Autonomía Local (Meses)"
            FROM AreaMapping a
            LEFT JOIN TotalBalance b ON a.material = b.material
            LEFT JOIN mb5b_initial_stock i ON a.material = TRIM(i.material)
            LEFT JOIN GlobalConsumption g ON a.material = g.material
            WHERE g.global_consumo_total > 0
              AND (COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(g.global_consumo_total / (SELECT m_count FROM MonthCount), 0) < 1.0
              AND NOT (UPPER(COALESCE(i.umb, '')) IN ('KG', 'GLN') AND (g.global_consumo_total / (SELECT m_count FROM MonthCount)) > 300)
              AND (SELECT m_count FROM MonthCount) / g.global_n_retiros <= 12.0
            ORDER BY a.area_negocio ASC, "Autonomía Local (Meses)" ASC;
            """

            result_main = self.session.execute(text(sql)).mappings().fetchall()
            result_areas = self.session.execute(text(sql_areas)).mappings().fetchall()

            df_main = pd.DataFrame([dict(row) for row in result_main])
            df_areas = pd.DataFrame([dict(row) for row in result_areas])

            return df_main, df_areas
        except Exception as e:
            logger.error(f"Error fetching replenishment export data: {e}")
            raise
