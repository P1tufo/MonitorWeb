import pandas as pd
from sqlalchemy import text
from .base import BaseRepository

class TasksRepository(BaseRepository):
    """Repositorio para el dominio de Tareas de Almacén."""

    def get_tasks_summary(self) -> pd.DataFrame:
        fallback = """
            SELECT 
                cl_mov as code,
                clase_mov as name,
                COUNT(*) as count,
                SUM(ctd_teor_dsd) as total_qty
            FROM warehouse_tasks
            WHERE cl_mov IS NOT NULL
            GROUP BY cl_mov, clase_mov
            ORDER BY count DESC
        """
        return pd.read_sql(self._sql("ots_summary_by_mov", fallback), self.session.connection().connection)

    def get_tasks_trend(self) -> pd.DataFrame:
        from datetime import datetime, timedelta
        today = datetime.now()
        first_of_this_month = today.replace(day=1)
        last_month = first_of_this_month - timedelta(days=1)
        start_period = last_month.strftime("%Y-%m")

        fallback = f"""
            SELECT 
                d.date as label,
                substr(d.date, 7, 4) || '-' || substr(d.date, 4, 2) || '-' || substr(d.date, 1, 2) as sort_key,
                (SELECT COUNT(*) FROM warehouse_tasks WHERE fe_creac = d.date) as created,
                (SELECT COUNT(*) FROM warehouse_tasks WHERE fecha_conf = d.date) as confirmed
            FROM (
                SELECT fe_creac as date FROM warehouse_tasks WHERE fe_creac IS NOT NULL AND fe_creac != ''
                UNION
                SELECT fecha_conf as date FROM warehouse_tasks WHERE fecha_conf IS NOT NULL AND fecha_conf != ''
            ) d
            WHERE sort_key >= '{start_period}-01'
            ORDER BY sort_key ASC
        """
        return pd.read_sql(self._sql("ots_daily_trend", fallback), self.session.connection().connection)

    def get_tasks_by_user(self) -> pd.DataFrame:
        from datetime import datetime, timedelta
        today = datetime.now()
        first_of_this_month = today.replace(day=1)
        last_month = first_of_this_month - timedelta(days=1)
        start_period = last_month.strftime("%Y-%m")

        fallback = f"""
            SELECT 
                u.user,
                (SELECT COUNT(*) FROM warehouse_tasks WHERE usuario = u.user AND substr(fe_creac, 7, 4) || '-' || substr(fe_creac, 4, 2) >= '{start_period}') as created,
                (SELECT COUNT(*) FROM warehouse_tasks WHERE usuario_conf = u.user AND substr(fecha_conf, 7, 4) || '-' || substr(fecha_conf, 4, 2) >= '{start_period}') as confirmed
            FROM (
                SELECT usuario as user FROM warehouse_tasks WHERE usuario IS NOT NULL AND usuario != ''
                UNION
                SELECT usuario_conf as user FROM warehouse_tasks WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
            ) u
            GROUP BY u.user
            HAVING created > 0 OR confirmed > 0
            ORDER BY (created + confirmed) DESC
            LIMIT 10
        """
        return pd.read_sql(self._sql("ots_by_user_dual", fallback), self.session.connection().connection)

    def get_tasks_by_type_dest(self) -> pd.DataFrame:
        from datetime import datetime, timedelta
        today = datetime.now()
        first_of_this_month = today.replace(day=1)
        last_month = first_of_this_month - timedelta(days=1)
        start_period = last_month.strftime("%Y-%m")

        fallback = f"""
            SELECT 
                clase_mov as type,
                COUNT(*) as count
            FROM warehouse_tasks
            WHERE cl_mov IS NOT NULL
            AND substr(fe_creac, 7, 4) || '-' || substr(fe_creac, 4, 2) >= '{start_period}'
            GROUP BY type
            ORDER BY count DESC
        """
        return pd.read_sql(self._sql("ots_by_movement_type", fallback), self.session.connection().connection)

    def get_recent_tasks(self) -> pd.DataFrame:
        fallback = """
            SELECT 
                numero_ot,
                material,
                texto_breve_material as material_name,
                clase_mov,
                ctd_teor_dsd as qty,
                ubic_proc as source,
                ubic_dest as dest,
                fe_creac || ' ' || hora as created_at,
                usuario as creator
            FROM warehouse_tasks
            WHERE (fecha_conf IS NULL OR fecha_conf = '')
            ORDER BY substr(fe_creac, 7, 4) ASC, substr(fe_creac, 4, 2) ASC, substr(fe_creac, 1, 2) ASC, hora ASC
        """
        return pd.read_sql(self._sql("ots_list_pending", fallback), self.session.connection().connection)

    def get_non_palletized_movements(self) -> pd.DataFrame:
        query = """
            SELECT 
                p.otcuanto as doc_mat,
                MAX(m.pos) as pos,
                MAX(p.material) as material,
                MAX(p.denominacion) as material_name,
                MAX(m.cmv) as clase_mov,
                MAX(p.stock_disp) as qty,
                MAX(m.alm) as source,
                MAX(m.ce) as dest,
                MAX(m.fe_contab || ' ' || m.hora) as created_at,
                MAX(m.usuario) as creator
            FROM lx02_pendientes p
            LEFT JOIN inventory_movements m ON p.otcuanto = m.doc_mat
            WHERE CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
            GROUP BY p.otcuanto
            ORDER BY created_at DESC
            LIMIT 100
        """
        try:
            return pd.read_sql(query, self.session.connection())
        except Exception:
            return pd.DataFrame()

    def get_non_palletized_count(self) -> int:
        query = """
            SELECT COUNT(p.material)
            FROM lx02_pendientes p
            JOIN (SELECT DISTINCT doc_mat FROM inventory_movements) m ON p.otcuanto = m.doc_mat
            WHERE CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
        """
        try:
            res = self.session.execute(text(query)).fetchone()
            return res[0] if res else 0
        except Exception:
            return 0

    def get_non_palletized_summary(self) -> pd.DataFrame:
        fallback = """SELECT 
                        m.usuario as user,
                        m.cmv as clase_mov,
                        COUNT(p.material) as count,
                        MIN(substr(m.fe_contab, 7, 4) || '-' || substr(m.fe_contab, 4, 2) || '-' || substr(m.fe_contab, 1, 2) || ' ' || m.hora) as oldest,
                        MAX(substr(m.fe_contab, 7, 4) || '-' || substr(m.fe_contab, 4, 2) || '-' || substr(m.fe_contab, 1, 2) || ' ' || m.hora) as newest
                    FROM lx02_pendientes p
                    JOIN (
                        SELECT doc_mat, usuario, cmv, MAX(fe_contab) as fe_contab, MAX(hora) as hora 
                        FROM inventory_movements 
                        GROUP BY doc_mat, usuario, cmv
                    ) m ON p.otcuanto = m.doc_mat
                    WHERE CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
                    GROUP BY m.usuario, m.cmv
                    ORDER BY clase_mov ASC, newest DESC"""
        try:
            final_sql = self._sql("inv_non_palletized_summary", fallback)
            df = pd.read_sql(final_sql, self.session.connection())
        except Exception:
            df = pd.DataFrame()
        
        def reformat_date(date_str):
            if not date_str or pd.isna(date_str):
                return "N/A"
            try:
                parts = date_str.split(' ')
                ymd = parts[0].split('-')
                hms = parts[1] if len(parts) > 1 else "00:00:00"
                return f"{ymd[2]}-{ymd[1]}-{ymd[0]} {hms}"
            except Exception:
                return date_str
                
        if not df.empty:
            df['oldest'] = df['oldest'].apply(reformat_date)
            df['newest'] = df['newest'].apply(reformat_date)
            
        return df
