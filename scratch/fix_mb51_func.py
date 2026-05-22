def _prepare_user_location_analytics(conn, anio, mes) -> Dict[str, Any]:
    """Estadísticas detalladas de usuarios y ubicaciones con actividad mensual."""
    p_mes = str(mes).zfill(2)
    p_anio = str(anio)
    
    # 1. Top Ubicaciones con desglose mensual
    query_loc = """
        SELECT COALESCE(ubicacion_fisica, 'S/U') as ubi, 
               COUNT(*) as total_qty,
               COUNT(CASE WHEN substr(fecontab,4,2)=? AND substr(fecontab,7,4)=? THEN 1 END) as qty_cm
        FROM mb51_transactions
        WHERE TRIM(cmv) = '201' AND ubi IS NOT NULL AND ubi != 'S/U'
        GROUP BY ubi
        ORDER BY total_qty DESC
        LIMIT 10
    """
    loc_stats = pd.read_sql(query_loc, conn, params=(p_mes, p_anio))
    loc_records = loc_stats.to_dict(orient="records")
    for r in loc_records:
        r['total_qty_fmt'] = fmt_num(r['total_qty'])

    # 2. Top Usuarios con desglose mensual
    query_user = """
        SELECT usuario as user, 
               COUNT(*) as qty,
               COUNT(CASE WHEN substr(fecontab,4,2)=? AND substr(fecontab,7,4)=? THEN 1 END) as qty_cm,
               SUM(CASE WHEN cmv IN ('202', '262') THEN 1 ELSE 0 END) as anulaciones
        FROM mb51_transactions
        WHERE TRIM(cmv) IN ('201', '261', '202', '262') AND usuario IS NOT NULL
        GROUP BY usuario
        ORDER BY qty DESC
        LIMIT 15
    """
    user_stats = pd.read_sql(query_user, conn, params=(p_mes, p_anio))
    user_records = user_stats.to_dict(orient="records")
    for u in user_records:
        u['qty_fmt'] = fmt_num(u.get('qty', 0))
        q = u.get('qty', 0) or 1
        u['error_rate'] = round((u.get('anulaciones', 0) / q) * 100, 1)

    return {"top_users": user_records, "top_ubicaciones_quick": loc_records}
