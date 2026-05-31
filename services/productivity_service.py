import logging
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any

logger = logging.getLogger("services-productivity")

class ProductivityService:
    def __init__(self, session: Session):
        self.session = session

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
            import pandas as pd
            from sqlalchemy import text
            df = pd.read_sql(text(query), self.session.connection())
            return df['date_iso'].dropna().tolist()
        except Exception as e:
            logger.error(f"Error en get_available_dates: {e}")
            return []

    def get_productivity_data(self, target_date: str) -> Dict[str, Any]:
        """
        Retorna todos los KPIs de productividad para una fecha específica (YYYY-MM-DD).
        """
        # Convertir YYYY-MM-DD a DD.MM.YYYY (formato de inventory_movements)
        try:
            import re
            # Si el formato es YYYY-MM-DD
            if re.match(r'^\d{4}-\d{2}-\d{2}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[2]}.{parts[1]}.{parts[0]}"
            # Si el formato es DD-MM-YYYY
            elif re.match(r'^\d{2}-\d{2}-\d{4}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[0]}.{parts[1]}.{parts[2]}"
            else:
                date_sap = target_date
        except:
            date_sap = target_date

        logger.info(f"Calculando KPIs de productividad para la fecha: {date_sap}")

        summary = self._get_daily_summary(date_sap)
        trend = self._get_hourly_trend(date_sap)
        gaps = self._get_inactivity_gaps(date_sap)
        heatmap = self._get_activity_heatmap(date_sap)

        return {
            "target_date": target_date,
            "target_date_sap": date_sap,
            "summary": summary,
            "trend": trend,
            "gaps": gaps,
            "heatmap": heatmap
        }

    def _get_daily_summary(self, date_sap: str) -> list:
        query = """
            WITH combined AS (
                SELECT 
                    usuario,
                    COUNT(doc_mat) as generado,
                    0 as confirmado,
                    MIN(hora) as min_hora,
                    MAX(hora) as max_hora
                FROM inventory_movements
                WHERE usuario IS NOT NULL AND usuario != '' 
                  AND registrado = :date_sap
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario
                
                UNION ALL
                
                SELECT 
                    usuario_conf as usuario,
                    0 as generado,
                    COUNT(numero_ot) as confirmado,
                    MIN(hor_conf) as min_hora,
                    MAX(hor_conf) as max_hora
                FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != '' 
                  AND fecha_conf = REPLACE(:date_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                GROUP BY usuario_conf
                
                UNION ALL

                SELECT 
                    usuario as usuario,
                    COUNT(numero_ot) as generado,
                    0 as confirmado,
                    MIN(hora) as min_hora,
                    MAX(hora) as max_hora
                FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != '' 
                  AND fe_creac = REPLACE(:date_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario
            )
            SELECT 
                usuario,
                SUM(generado) as movimientos_generados,
                SUM(confirmado) as tareas_confirmadas,
                (SUM(generado) + SUM(confirmado)) as total_actividad,
                MIN(min_hora) as primer_movimiento,
                MAX(max_hora) as ultimo_movimiento,
                ROUND((julianday('2000-01-01 ' || MAX(max_hora)) - julianday('2000-01-01 ' || MIN(min_hora))) * 24 * 60, 0) as tiempo_total_minutos
            FROM combined
            GROUP BY usuario
            ORDER BY total_actividad DESC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap})
            # Limpiar NaNs
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en _get_daily_summary: {e}")
            return []

    def _get_hourly_trend(self, date_sap: str) -> list:
        query = """
            WITH combined AS (
                SELECT 
                    substr(hora, 1, 2) as franja_horaria,
                    COUNT(doc_mat) as movimientos
                FROM inventory_movements
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND registrado = :date_sap
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY franja_horaria
                
                UNION ALL
                
                SELECT 
                    substr(hor_conf, 1, 2) as franja_horaria,
                    COUNT(numero_ot) as movimientos
                FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
                  AND fecha_conf = REPLACE(:date_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                GROUP BY franja_horaria
                
                UNION ALL

                SELECT 
                    substr(hora, 1, 2) as franja_horaria,
                    COUNT(numero_ot) as movimientos
                FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND fe_creac = REPLACE(:date_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY franja_horaria
            )
            SELECT 
                franja_horaria,
                SUM(movimientos) as total_actividad
            FROM combined
            GROUP BY franja_horaria
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
        query = """
            WITH AllActivities AS (
                SELECT usuario, hora, doc_mat FROM inventory_movements 
                WHERE usuario IS NOT NULL AND usuario != '' AND registrado = :date_sap AND hora IS NOT NULL AND hora != ''
                UNION ALL
                SELECT usuario_conf as usuario, hor_conf as hora, numero_ot as doc_mat FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != '' AND fecha_conf = REPLACE(:date_sap, '.', '-') AND hor_conf IS NOT NULL AND hor_conf != ''
                UNION ALL
                SELECT usuario, hora, numero_ot as doc_mat FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != '' AND fe_creac = REPLACE(:date_sap, '.', '-') AND hora IS NOT NULL AND hora != ''
            ),
            Ranked AS (
                SELECT 
                    usuario,
                    hora,
                    doc_mat,
                    LAG(hora) OVER (PARTITION BY usuario ORDER BY hora) as hora_anterior
                FROM AllActivities
                WHERE LOWER(usuario) NOT IN ('cvalderrama', 'e_sperezb', 'gmolina')
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
        # Igual que el hourly trend pero basado en cantidad de movimientos en lugar de doc_mat distintos
        query = """
            WITH Rearmed AS (
                SELECT 
                    usuario,
                    substr(hora, 1, 2) as franja_horaria,
                    COUNT(doc_mat) as generado,
                    0 as confirmado
                FROM inventory_movements
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND registrado = :date_sap
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario, franja_horaria
                
                UNION ALL
                
                SELECT 
                    usuario_conf as usuario,
                    substr(hor_conf, 1, 2) as franja_horaria,
                    0 as generado,
                    COUNT(numero_ot) as confirmado
                FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
                  AND fecha_conf = REPLACE(:date_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                GROUP BY usuario_conf, franja_horaria

                UNION ALL

                SELECT 
                    usuario,
                    substr(hora, 1, 2) as franja_horaria,
                    COUNT(numero_ot) as generado,
                    0 as confirmado
                FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND fe_creac = REPLACE(:date_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario, franja_horaria
            )
            SELECT 
                usuario,
                franja_horaria,
                SUM(generado) + SUM(confirmado) as cantidad_movimientos,
                SUM(generado) as generados,
                SUM(confirmado) as confirmados
            FROM Rearmed
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
        try:
            import re
            if re.match(r'^\d{4}-\d{2}-\d{2}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[2]}.{parts[1]}.{parts[0]}"
            elif re.match(r'^\d{2}-\d{2}-\d{4}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[0]}.{parts[1]}.{parts[2]}"
            else:
                date_sap = target_date
        except:
            date_sap = target_date

        query = """
            WITH combined AS (
                SELECT 
                    'Inventario (MB51)' as origen,
                    COALESCE(tipo_operacion, texto_cab_documento) as operacion,
                    doc_mat
                FROM inventory_movements
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND registrado = :date_sap
                  AND hora IS NOT NULL AND hora != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Confirmación OT' as operacion,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario_conf) = UPPER(:usuario)
                  AND fecha_conf = REPLACE(:date_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Creación OT' as operacion,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND fe_creac = REPLACE(:date_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
            )
            SELECT origen, operacion, COUNT(*) as cantidad
            FROM combined 
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
        try:
            import re
            if re.match(r'^\d{4}-\d{2}-\d{2}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[2]}.{parts[1]}.{parts[0]}"
            elif re.match(r'^\d{2}-\d{2}-\d{4}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[0]}.{parts[1]}.{parts[2]}"
            else:
                date_sap = target_date
        except:
            date_sap = target_date

        query = """
            WITH combined AS (
                SELECT 
                    'Inventario (MB51)' as origen,
                    COALESCE(tipo_operacion, texto_cab_documento) as operacion,
                    cmv,
                    material,
                    texto_breve_material as descripcion,
                    cantidad,
                    hora,
                    doc_mat
                FROM inventory_movements
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND registrado = :date_sap
                  AND hora IS NOT NULL AND hora != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Confirmación OT' as operacion,
                    '-' as cmv,
                    material,
                    texto_breve_material as descripcion,
                    ctd_teor_dsd as cantidad,
                    hor_conf as hora,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario_conf) = UPPER(:usuario)
                  AND fecha_conf = REPLACE(:date_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Creación OT' as operacion,
                    '-' as cmv,
                    material,
                    texto_breve_material as descripcion,
                    ctd_teor_dsd as cantidad,
                    hora as hora,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND fe_creac = REPLACE(:date_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
            )
            SELECT * FROM combined 
            WHERE operacion = :operacion
            ORDER BY hora ASC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"date_sap": date_sap, "usuario": usuario, "operacion": operacion})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en get_user_movements_daily_details: {e}")
            return []

    def get_monthly_productivity_data(self, target_month: str) -> Dict[str, Any]:
        """
        Retorna todos los KPIs de productividad para un mes específico (YYYY-MM).
        """
        try:
            parts = target_month.split('-')
            month_sap = f"{parts[1]}.{parts[0]}"
        except:
            month_sap = target_month

        logger.info(f"Calculando KPIs de productividad para el mes: {month_sap}")

        summary = self._get_monthly_summary(month_sap)
        shifts = self._get_monthly_shifts(month_sap)
        heatmap = self._get_monthly_heatmap(month_sap)

        return {
            "target_month": target_month,
            "target_month_sap": month_sap,
            "summary": summary,
            "shifts": shifts,
            "heatmap": heatmap
        }

    def _get_monthly_summary(self, month_sap: str) -> list:
        query = """
            WITH combined AS (
                SELECT 
                    usuario,
                    registrado as fecha,
                    COUNT(doc_mat) as generado,
                    0 as confirmado
                FROM inventory_movements
                WHERE usuario IS NOT NULL AND usuario != '' 
                  AND registrado LIKE :month_sap
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario, registrado
                
                UNION ALL
                
                SELECT 
                    usuario_conf as usuario,
                    REPLACE(fecha_conf, '-', '.') as fecha,
                    0 as generado,
                    COUNT(numero_ot) as confirmado
                FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != '' 
                  AND fecha_conf LIKE REPLACE(:month_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                GROUP BY usuario_conf, fecha_conf

                UNION ALL

                SELECT 
                    usuario,
                    REPLACE(fe_creac, '-', '.') as fecha,
                    COUNT(numero_ot) as generado,
                    0 as confirmado
                FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != '' 
                  AND fe_creac LIKE REPLACE(:month_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario, fe_creac
            )
            SELECT 
                usuario,
                SUM(generado) as movimientos_generados,
                SUM(confirmado) as tareas_confirmadas,
                (SUM(generado) + SUM(confirmado)) as total_actividad,
                COUNT(DISTINCT fecha) as dias_trabajados,
                ROUND(CAST((SUM(generado) + SUM(confirmado)) AS FLOAT) / COUNT(DISTINCT fecha), 1) as promedio_actividad_dia
            FROM combined
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
        query = """
            WITH combined AS (
                SELECT 
                    registrado as fecha,
                    CASE
                        WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 6 AND 13 THEN 'Mañana'
                        WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 14 AND 21 THEN 'Tarde'
                        ELSE 'Noche'
                    END as turno,
                    COUNT(doc_mat) as actividad
                FROM inventory_movements
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND registrado LIKE :month_sap
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY registrado, turno
                
                UNION ALL
                
                SELECT 
                    REPLACE(fecha_conf, '-', '.') as fecha,
                    CASE
                        WHEN CAST(substr(hor_conf, 1, 2) AS INTEGER) BETWEEN 6 AND 13 THEN 'Mañana'
                        WHEN CAST(substr(hor_conf, 1, 2) AS INTEGER) BETWEEN 14 AND 21 THEN 'Tarde'
                        ELSE 'Noche'
                    END as turno,
                    COUNT(numero_ot) as actividad
                FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
                  AND fecha_conf LIKE REPLACE(:month_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                GROUP BY fecha_conf, turno

                UNION ALL

                SELECT 
                    REPLACE(fe_creac, '-', '.') as fecha,
                    CASE
                        WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 6 AND 13 THEN 'Mañana'
                        WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 14 AND 21 THEN 'Tarde'
                        ELSE 'Noche'
                    END as turno,
                    COUNT(numero_ot) as actividad
                FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND fe_creac LIKE REPLACE(:month_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY fe_creac, turno
            )
            SELECT 
                fecha,
                turno,
                SUM(actividad) as total_actividad
            FROM combined
            GROUP BY fecha, turno
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
        # Calcular el día de la semana (0=Domingo, 1=Lunes, ... 6=Sábado)
        # SQLite no tiene una función nativa para parsear DD.MM.YYYY directo a weekday
        # Pero podemos usar substr para rearmar a YYYY-MM-DD y usar strftime
        query = """
            WITH Rearmed AS (
                SELECT 
                    usuario,
                    substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || '-' || substr(registrado, 1, 2) as date_iso,
                    COUNT(doc_mat) as generado,
                    0 as confirmado
                FROM inventory_movements
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND registrado LIKE :month_sap
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario, date_iso
                
                UNION ALL
                
                SELECT 
                    usuario_conf as usuario,
                    substr(fecha_conf, 7, 4) || '-' || substr(fecha_conf, 4, 2) || '-' || substr(fecha_conf, 1, 2) as date_iso,
                    0 as generado,
                    COUNT(numero_ot) as confirmado
                FROM warehouse_tasks
                WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
                  AND fecha_conf LIKE REPLACE(:month_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                GROUP BY usuario_conf, date_iso

                UNION ALL

                SELECT 
                    usuario,
                    substr(fe_creac, 7, 4) || '-' || substr(fe_creac, 4, 2) || '-' || substr(fe_creac, 1, 2) as date_iso,
                    COUNT(numero_ot) as generado,
                    0 as confirmado
                FROM warehouse_tasks
                WHERE usuario IS NOT NULL AND usuario != ''
                  AND fe_creac LIKE REPLACE(:month_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
                GROUP BY usuario, date_iso
            )
            SELECT 
                usuario,
                CAST(strftime('%w', date_iso) AS INTEGER) as dia_semana,
                SUM(generado) + SUM(confirmado) as cantidad_movimientos,
                SUM(generado) as generados,
                SUM(confirmado) as confirmados
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
        try:
            parts = target_month.split('-')
            month_sap = f"{parts[1]}.{parts[0]}"
        except:
            month_sap = target_month

        query = """
            WITH combined AS (
                SELECT 
                    'Inventario (MB51)' as origen,
                    COALESCE(tipo_operacion, texto_cab_documento) as operacion,
                    doc_mat
                FROM inventory_movements
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND registrado LIKE :month_sap
                  AND hora IS NOT NULL AND hora != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Confirmación OT' as operacion,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario_conf) = UPPER(:usuario)
                  AND fecha_conf LIKE REPLACE(:month_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Creación OT' as operacion,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND fe_creac LIKE REPLACE(:month_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
            )
            SELECT origen, operacion, COUNT(*) as cantidad
            FROM combined 
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
        try:
            parts = target_month.split('-')
            month_sap = f"{parts[1]}.{parts[0]}"
        except:
            month_sap = target_month

        query = """
            WITH combined AS (
                SELECT 
                    'Inventario (MB51)' as origen,
                    COALESCE(tipo_operacion, texto_cab_documento) as operacion,
                    cmv,
                    material,
                    texto_breve_material as descripcion,
                    cantidad,
                    registrado as fecha,
                    hora,
                    doc_mat
                FROM inventory_movements
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND registrado LIKE :month_sap
                  AND hora IS NOT NULL AND hora != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Confirmación OT' as operacion,
                    '-' as cmv,
                    material,
                    texto_breve_material as descripcion,
                    ctd_teor_dsd as cantidad,
                    REPLACE(fecha_conf, '-', '.') as fecha,
                    hor_conf as hora,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario_conf) = UPPER(:usuario)
                  AND fecha_conf LIKE REPLACE(:month_sap, '.', '-')
                  AND hor_conf IS NOT NULL AND hor_conf != ''
                UNION ALL
                SELECT 
                    'Tarea Almacén (WMS)' as origen,
                    'Creación OT' as operacion,
                    '-' as cmv,
                    material,
                    texto_breve_material as descripcion,
                    ctd_teor_dsd as cantidad,
                    REPLACE(fe_creac, '-', '.') as fecha,
                    hora as hora,
                    numero_ot as doc_mat
                FROM warehouse_tasks
                WHERE UPPER(usuario) = UPPER(:usuario)
                  AND fe_creac LIKE REPLACE(:month_sap, '.', '-')
                  AND hora IS NOT NULL AND hora != ''
            )
            SELECT * FROM combined 
            WHERE operacion = :operacion
            ORDER BY substr(fecha, 7, 4) || substr(fecha, 4, 2) || substr(fecha, 1, 2) ASC, hora ASC
        """
        try:
            df = pd.read_sql(text(query), self.session.connection(), params={"usuario": usuario, "month_sap": f"%.{month_sap}", "operacion": operacion})
            df = df.astype(object).where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error en get_user_movements_monthly_details: {e}")
            return []
