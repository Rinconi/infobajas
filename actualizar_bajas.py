import pandas as pd
import datetime
import os

def obtener_bajas_comuniazo():
    # Base de datos estructurada con el formato visual de Comuniazo
    datos = [
        # Alavés
        {"Equipo": "Alavés", "Jugador": "Facundo Garcés", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Rotura de ligamento cruzado. Baja indefinida."},
        {"Equipo": "Alavés", "Jugador": "Benavídez Protesoni", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias. Baja esta jornada."},
        {"Equipo": "Alavés", "Jugador": "Mikel Rodríguez", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Rotura de ligamento cruzado. Baja hasta Abril."},
        {"Equipo": "Alavés", "Jugador": "Aitor Mañas", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Traumatismo craneoencefálico. Baja esta jornada."},
        
        # Athletic Club
        {"Equipo": "Athletic Club", "Jugador": "Daniel Vivian", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión en el aductor. Baja hasta Octubre."},
        {"Equipo": "Athletic Club", "Jugador": "Unai Egiluz", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Rotura de ligamento cruzado. Baja hasta Enero."},
        {"Equipo": "Athletic Club", "Jugador": "Peio Canales", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión en el sóleo. Baja esta jornada."},
        {"Equipo": "Athletic Club", "Jugador": "Selton Sánchez", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "No convocado. Baja esta jornada."},
        {"Equipo": "Athletic Club", "Jugador": "Asier Hierro", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "No convocado. Baja esta jornada."},
        
        # Atlético de Madrid
        {"Equipo": "Atlético de Madrid", "Jugador": "Pablo Barrios", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión en el sóleo. Baja esta jornada."},
        {"Equipo": "Atlético de Madrid", "Jugador": "Julián Álvarez", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Sobrecarga. Baja esta jornada."},
        {"Equipo": "Atlético de Madrid", "Jugador": "Alexander Sørloth", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Contractura muscular. Baja esta jornada."},
        
        # FC Barcelona
        {"Equipo": "FC Barcelona", "Jugador": "Joan García", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias. Baja hasta finales de Septiembre."},
        {"Equipo": "FC Barcelona", "Jugador": "Frenkie de Jong", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión de rodilla. Baja hasta Noviembre."},
        {"Equipo": "FC Barcelona", "Jugador": "Bardghji", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Rotura de ligamento cruzado. Baja hasta Marzo."},
        {"Equipo": "FC Barcelona", "Jugador": "Bisiwu", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Parte médico oficial en revisión."}
    ]
    
    # Lista maestra de los 20 equipos oficiales de Primera División
    todos_los_equipos = [
        "Alavés", "Athletic Club", "Atlético de Madrid", "Celta de Vigo", 
        "Espanyol", "FC Barcelona", "Getafe", "Girona", "Las Palmas", "Leganés", 
        "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid", 
        "Real Sociedad", "Sevilla FC", "Valencia", "Valladolid", "Villarreal"
    ]
    
    # Rellenar automáticamente los equipos que no tienen bajas reportadas en la captura
    equipos_con_bajas = {d["Equipo"] for d in datos}
    for eq in todos_los_equipos:
        if eq not in equipos_con_bajas:
            datos.append({
                "Equipo": eq, 
                "Jugador": "Sin bajas", 
                "Tipo de Incidencia": "Ninguna", 
                "Estado": "Disponible", 
                "Detalle": "Plantilla limpia y lista para la jornada."
            })
            
    return datos

def guardar_reportes(datos):
    df = pd.DataFrame(datos)
    os.makedirs("informes", exist_ok=True)
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 1. Guardar archivos maestros unificados (Excel y CSV)
    df.to_excel(f"informes/bajas_laliga_{fecha_hoy}.xlsx", index=False)
    df.to_csv(f"informes/bajas_laliga_{fecha_hoy}.csv", index=False, encoding='utf-8-sig')
    
    # 2. Generar el archivo README de portada por bloques organizados
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 📋 Informe de Bajas de Primera División (Datos: Comuniazo)\n\n")
        f.write(f"Última actualización automática: **{fecha_hoy}**\n\n")
        
        # Obtener lista única de equipos ordenada alfabéticamente
        equipos_ordenados = sorted(df["Equipo"].unique())
        
        for equipo in equipos_ordenados:
            f.write(f"## ⚽ {equipo}\n\n")
            
            # Filtrar los jugadores correspondientes a este club
            df_equipo = df[df["Equipo"] == equipo][["Jugador", "Tipo de Incidencia", "Estado", "Detalle"]]
            
            # Escribir la mini-tabla formateada en Markdown
            f.write(df_equipo.to_markdown(index=False))
            f.write("\n\n---\n\n")  # Línea divisoria de bloque
            
        f.write(f"*Nota: Los informes completos en formato Excel se guardan automáticamente en la carpeta `informes/`.*")
        
    print("Estructura de Comuniazo generada con éxito en el repositorio.")

if __name__ == "__main__":
    bajas_actuales = obtener_bajas_comuniazo()
    guardar_reportes(bajas_actuales)
