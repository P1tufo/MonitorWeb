import logging
import re

import pandas as pd
from sqlalchemy import text

from core.macros import EXCLUDED_USERS_INACTIVITY

from .base import BaseRepository

logger = logging.getLogger("repo-productivity")

class ProductivityRepository(BaseRepository):
    """Repositorio para el dominio de Analíticas de Productividad de Usuarios."""

    def _get_raw_activities_cte(self, is_monthly=False) -> str:
        """
        Retorna la CTE base unificada con todos los eventos de actividad.
        Evita el código SQL duplicado masivo que había anteriormente.
        """
        op = "LIKE :month_sap" if is_monthly else "= :date_sap"
        replace_op = "LIKE REPLACE(:month_sap, '.', '-')" if is_monthly else "= REPLACE(:date_sap, '.', '-')"

        return f"""
            AllActivities AS (
                SELECT
                    usuario,
                    registrado as fecha,
                    hora,
                    doc_mat,
                    'Inventario (MB51)' as origen,
                    COALESCE(tipo_operacion, texto_cab_documento) as operacion,
                    1 as es_generado,
                    0 as es_confirmado,
                    cmv,
                    material,
                    texto_breve_material as descripcion,
                    cantidad
                FROM inventory_movements
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND registrado {op}
                  AND hora IS NOT NULL AND hora != ''

                UNION ALL

                SELECT
                    usuario_conf as usuario,
                    REPLACE(fecha_conf, '-', '.') as fecha,
                    hor_conf as hora,
                    numero_ot as doc_mat,
                    'Tarea Almacén (WMS)' as origen,
                    'Confirmación OT' as operacion,
                    0 as es_generado,
                    1 as es_confirmado,
                    '-' as cmv,
                    material,
                    texto_breve_material as descripcion,
                    ctd_teor_dsd as cantidad
                FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
                  AND fecha_conf {replace_op}
                  AND hor_conf IS NOT NULL AND hor_conf != ''

                UNION ALL

                SELECT
                    usuario,
                    REPLACE(fe_creac, '-', '.') as fecha,
                    hora,
                    numero_ot as doc_mat,
                    'Tarea Almacén (WMS)' as origen,
                    'Creación OT' as operacion,
                    1 as es_generado,
                    0 as es_confirmado,
                    '-' as cmv,
                    material,
                    texto_breve_material as descripcion,
                    ctd_teor_dsd as cantidad
                FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND fe_creac {replace_op}
                  AND hora IS NOT NULL AND hora != ''
            )
        """

    def get_available_dates(self) -> list:
        """
        Returns a sorted list of unique dates (YYYY-MM-DD format) that have either
        generated or confirmed movements.
        """
        query = """
            SELECT DISTINCT substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || '-' || substr(registrado, 1, 2) as date_iso
            FROM inventory_movements
            WHERE registrado IS NOT NULL AND registrado != ''

            UNION

            SELECT DISTINCT substr(fecha_conf, 7, 4) || '-' || substr(fecha_conf, 4, 2) || '-' || substr(fecha_conf, 1, 2) as date_iso
            FROM warehouse_tasks
            WHERE fecha_conf IS NOT NULL AND fecha_conf != ''

            ORDER BY date_iso DESC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection())
            return df['date_iso'].dropna().tolist()
        except Exception as e:
            logger.error(f"Error en get_available_dates: {e}")
            return []

    def get_all_users(self) -> list:
        """
        Retorna la lista completa de usuarios que han tenido alguna actividad
        (inventario o almacén) para poblar los filtros y agrupaciones.
        """
        query = """
            SELECT DISTINCT usuario FROM inventory_movements WHERE usuario IS NOT NULL AND usuario != ''
            UNION
            SELECT DISTINCT usuario_conf FROM warehouse_tasks WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
            UNION
            SELECT DISTINCT usuario FROM warehouse_tasks WHERE usuario IS NOT NULL AND usuario != ''
            ORDER BY usuario ASC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection())
            return df['usuario'].dropna().tolist()
        except Exception as e:
            logger.error(f"Error en get_all_users: {e}")
            return []

    # --- DAILY PRODUCTIVITY ---

    def _get_daily_summary(self, date_sap: str) -> list:
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=False)}
            SELECT
                usuario,
                SUM(es_generado) as movimientos_generados,
                SUM(es_confirmado) as tareas_confirmadas,
                COUNT(*) as total_actividad,
                MIN(hora) as primer_movimiento,
                MAX(hora) as ultimo_movimiento,
                ROUND((julianday('2000-01-01 ' || MAX(hora)) - julianday('2000-01-01 ' || MIN(hora))) * 24 * 60, 0) as tiempo_total_minutos
            FROM AllActivities
            GROUP BY usuario
            ORDER BY total_actividad DESC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_daily_summary: {e}")
            return []

    def _get_hourly_trend(self, date_sap: str) -> list:
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=False)}
            SELECT
                usuario,
                substr(hora, 1, 2) as franja_horaria,
                COUNT(*) as total_actividad
            FROM AllActivities
            GROUP BY usuario, franja_horaria
            ORDER BY franja_horaria ASC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_hourly_trend: {e}")
            return []

    def _get_inactivity_gaps(self, date_sap: str) -> list:
        users_tuple = tuple(u.lower() for u in EXCLUDED_USERS_INACTIVITY)

        # SQLite IN no maneja listas directas en SQLAlchemy text tan fácilmente sin params variables,
        # así que la inyectamos si está securizada.
        excluded_str = ", ".join(f"'{u}'" for u in users_tuple)

        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=False)},
            Ranked AS (
                SELECT
                    usuario,
                    hora,
                    doc_mat,
                    LAG(hora) OVER (PARTITION BY usuario ORDER BY hora) as hora_anterior
                FROM AllActivities
                WHERE LOWER(usuario) NOT IN ({excluded_str})
            )
            SELECT
                usuario,
                hora_anterior,
                hora as hora_actual,
                ROUND((julianday('2000-01-01 ' || hora) - julianday('2000-01-01 ' || hora_anterior)) * 24 * 60, 0) as hueco_minutos,
                doc_mat
            FROM Ranked
            WHERE hora_anterior IS NOT NULL
              AND ROUND((julianday('2000-01-01 ' || hora) - julianday('2000-01-01 ' || hora_anterior)) * 24 * 60, 0) > 180
            ORDER BY hueco_minutos DESC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_inactivity_gaps: {e}")
            return []

    def _get_activity_heatmap(self, date_sap: str) -> list:
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=False)}
            SELECT
                usuario,
                substr(hora, 1, 2) as franja_horaria,
                COUNT(*) as cantidad_movimientos,
                SUM(es_generado) as generados,
                SUM(es_confirmado) as confirmados
            FROM AllActivities
            GROUP BY usuario, franja_horaria
            ORDER BY usuario, franja_horaria
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_activity_heatmap: {e}")
            return []

    def get_user_movements_daily_summary(self, target_date: str, usuario: str) -> list:
        date_sap = self._format_date_sap(target_date)
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=False)}
            SELECT origen, operacion, COUNT(*) as cantidad
            FROM AllActivities
            WHERE UPPER(usuario) = UPPER(:usuario)
            GROUP BY origen, operacion
            ORDER BY cantidad DESC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap, "usuario": usuario})
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en get_user_movements_daily_summary: {e}")
            return []

    def get_user_movements_daily_details(self, target_date: str, usuario: str, operacion: str) -> list:
        date_sap = self._format_date_sap(target_date)
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=False)}
            SELECT origen, operacion, cmv, material, descripcion, cantidad, hora, doc_mat
            FROM AllActivities
            WHERE UPPER(usuario) = UPPER(:usuario)
              AND operacion = :operacion
            ORDER BY hora ASC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap, "usuario": usuario, "operacion": operacion})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en get_user_movements_daily_details: {e}")
            return []

    # --- MONTHLY PRODUCTIVITY ---

    def _get_monthly_summary(self, month_sap: str) -> list:
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=True)}
            SELECT
                usuario,
                SUM(es_generado) as movimientos_generados,
                SUM(es_confirmado) as tareas_confirmadas,
                COUNT(*) as total_actividad,
                COUNT(DISTINCT fecha) as dias_trabajados,
                ROUND(CAST(COUNT(*) AS FLOAT) / COUNT(DISTINCT fecha), 1) as promedio_actividad_dia
            FROM AllActivities
            GROUP BY usuario
            ORDER BY total_actividad DESC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"month_sap": f"%.{month_sap}"})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_monthly_summary: {e}")
            return []

    def _get_monthly_shifts(self, month_sap: str) -> list:
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=True)}
            SELECT
                usuario,
                fecha,
                CASE
                    WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 6 AND 13 THEN 'Mañana'
                    WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 14 AND 21 THEN 'Tarde'
                    ELSE 'Noche'
                END as turno,
                COUNT(*) as total_actividad
            FROM AllActivities
            GROUP BY usuario, fecha, turno
            ORDER BY substr(fecha, 7, 4), substr(fecha, 4, 2), substr(fecha, 1, 2)
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"month_sap": f"%.{month_sap}"})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_monthly_shifts: {e}")
            return []

    def _get_monthly_heatmap(self, month_sap: str) -> list:
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=True)},
            Rearmed AS (
                SELECT
                    usuario,
                    substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2) as date_iso,
                    es_generado,
                    es_confirmado
                FROM AllActivities
            )
            SELECT
                usuario,
                CAST(strftime('%w', date_iso) AS INTEGER) as dia_semana,
                COUNT(*) as cantidad_movimientos,
                SUM(es_generado) as generados,
                SUM(es_confirmado) as confirmados
            FROM Rearmed
            GROUP BY usuario, dia_semana
            ORDER BY usuario, dia_semana
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"month_sap": f"%.{month_sap}"})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_monthly_heatmap: {e}")
            return []

    def get_user_movements_monthly_summary(self, target_month: str, usuario: str) -> list:
        month_sap = self._format_month_sap(target_month)
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=True)}
            SELECT origen, operacion, COUNT(*) as cantidad
            FROM AllActivities
            WHERE UPPER(usuario) = UPPER(:usuario)
            GROUP BY origen, operacion
            ORDER BY cantidad DESC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"usuario": usuario, "month_sap": f"%.{month_sap}"})
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en get_user_movements_monthly_summary: {e}")
            return []

    def get_user_movements_monthly_details(self, target_month: str, usuario: str, operacion: str) -> list:
        month_sap = self._format_month_sap(target_month)
        query = f"""
            WITH {self._get_raw_activities_cte(is_monthly=True)}
            SELECT origen, operacion, cmv, material, descripcion, cantidad, fecha, hora, doc_mat
            FROM AllActivities
            WHERE UPPER(usuario) = UPPER(:usuario)
              AND operacion = :operacion
            ORDER BY substr(fecha, 7, 4) || substr(fecha, 4, 2) || substr(fecha, 1, 2) ASC, hora ASC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"usuario": usuario, "month_sap": f"%.{month_sap}", "operacion": operacion})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en get_user_movements_monthly_details: {e}")
            return []

    # --- UTILS ---

    def _format_date_sap(self, target_date: str) -> str:
        if re.match(r'^\d{4}-\d{2}-\d{2}$', target_date):
            parts = target_date.split('-')
            return f"{parts[2]}.{parts[1]}.{parts[0]}"
        elif re.match(r'^\d{2}-\d{2}-\d{4}$', target_date):
            parts = target_date.split('-')
            return f"{parts[0]}.{parts[1]}.{parts[2]}"
        return target_date

    def _format_month_sap(self, target_month: str) -> str:
        if re.match(r'^\d{4}-\d{2}$', target_month):
            parts = target_month.split('-')
            return f"{parts[1]}.{parts[0]}"
        return target_month
