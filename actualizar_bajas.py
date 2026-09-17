import pandas as pd
import datetime
import os

def obtener_bajas_primera_division():
    # Base de datos manual extendida y verídica con los lesionados y sancionados de Primera División
    datos = [
        # Alavés
        {"Equipo": "Alavés", "Jugador": "Hugo Novoa", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias en el pubis"},
        {"Equipo": "Alavés", "Jugador": "Aitor Mañas", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Parte médico oficial pendiente"},
        {"Equipo": "Alavés", "Jugador": "Abqar", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias físicas"},
        
        # Athletic Club
        {"Equipo": "Athletic Club", "Jugador": "Unai Simón", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Operado de la muñeca"},
        {"Equipo": "Athletic Club", "Jugador": "Dani Vivian", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión en el aductor"},
        {"Equipo": "Athletic Club", "Jugador": "Unai Egiluz", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Rotura de ligamento cruzado anterior"},
        
        # Atlético de Madrid
        {"Equipo": "Atlético de Madrid", "Jugador": "Pablo Barrios", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión muscular en el sóleo"},
        
        # Celta de Vigo
        {"Equipo": "Celta de Vigo", "Jugador": "Iago Aspas", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Problemas físicos confirmados"},
        {"Equipo": "Celta de Vigo", "Jugador": "Antañón", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión muscular"},
        
        # Deportivo (Sanciones/Otros)
        {"Equipo": "Deportivo", "Jugador": "Angeliño", "Tipo de Incidencia": "Disciplinaria (Sanción)", "Estado": "Baja", "Detalle": "Tarjeta roja directa"},
        
        # Espanyol
        {"Equipo": "Espanyol", "Jugador": "Javi Puado", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias musculares"},
        {"Equipo": "Espanyol", "Jugador": "Kike García", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Baja de larga duración hasta 2027"},
        {"Equipo": "Espanyol", "Jugador": "Gorosabel", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Problemas físicos"},
        {"Equipo": "Espanyol", "Jugador": "Jofre", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Esguince leve"},
        {"Equipo": "Espanyol", "Jugador": "Omar El Hilali", "Tipo de Incidencia": "Disciplinaria (Sanción)", "Estado": "Baja", "Detalle": "Tarjeta roja directa"},
        
        # FC Barcelona
        {"Equipo": "FC Barcelona", "Jugador": "Dani Olmo", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión en el bíceps femoral"},
        {"Equipo": "FC Barcelona", "Jugador": "Fermín López", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión en el recto anterior"},
        {"Equipo": "FC Barcelona", "Jugador": "Marc Bernal", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Rotura de ligamento cruzado"},
        {"Equipo": "FC Barcelona", "Jugador": "Frenkie de Jong", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión grave de rodilla (Baja hasta 2027)"},
        {"Equipo": "FC Barcelona", "Jugador": "Joan García", "Tipo de Incidencia": "Física / Médica", "Estado": "Duda", "Detalle": "Leves molestias en la rodilla derecha"},
        
        # Getafe
        {"Equipo": "Getafe", "Jugador": "Uche", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión grave (Baja para toda la temporada)"},
        {"Equipo": "Getafe", "Jugador": "Juanmi Jiménez", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Dolencias musculares"},
        {"Equipo": "Getafe", "Jugador": "Kiko Femenía", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Sobrecarga"},
        
        # Osasuna
        {"Equipo": "Osasuna", "Jugador": "Valentín Rosier", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Problemas musculares"},
        {"Equipo": "Osasuna", "Jugador": "Aimar Oroz", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias en el muslo"},
        {"Equipo": "Osasuna", "Jugador": "Herrando", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Esguince de tobillo"},
        {"Equipo": "Osasuna", "Jugador": "Moi Gómez", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión fibrilar"},
        
        # Real Betis
        {"Equipo": "Real Betis", "Jugador": "Aitor Ruibal", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión muscular en el aductor"},
        
        # Real Madrid
        {"Equipo": "Real Madrid", "Jugador": "Eduardo Camavinga", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Esguince de rodilla"},
        {"Equipo": "Real Madrid", "Jugador": "Dani Ceballos", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Esguince de tobillo"},
        {"Equipo": "Real Madrid", "Jugador": "Éder Militão", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Proceso de recuperación muscular"},
        {"Equipo": "Real Madrid", "Jugador": "Rodrygo Goes", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Trabajo específico en el gimnasio"},
        {"Equipo": "Real Madrid", "Jugador": "Ferland Mendy", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias musculares"},
        
        # Real Sociedad
        {"Equipo": "Real Sociedad", "Jugador": "Hamari Traoré", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Rotura de ligamento cruzado"},
        {"Equipo": "Real Sociedad", "Jugador": "Odriozola", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Problemas físicos"},
        
        # Sevilla FC
        {"Equipo": "Sevilla FC", "Jugador": "Lucas Stassin", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Lesión miofascial en el aductor largo"},
        {"Equipo": "Sevilla FC", "Jugador": "Kike Salas", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Contusión (Trabajo específico)"},
        {"Equipo": "Sevilla FC", "Jugador": "Rubén Vargas", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Esguince de tobillo"},
        {"Equipo": "Sevilla FC", "Jugador": "Sangante", "Tipo de Incidencia": "Física / Médica", "Estado": "Baja", "Detalle": "Molestias en la rodilla"}
    ]
    return datos

def guardar_reportes(datos):
    # Creamos el DataFrame
    df = pd.DataFrame(datos)
    
    # ORDENAR POR EQUIPO ALFABÉTICAMENTE (Y por jugador en caso de empate)
    df = df.sort_values(by=["Equipo", "Jugador"])
    
    # Crear la carpeta de históricos si no existe
    os.makedirs("informes", exist_ok=True)
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Guardar los archivos físicos estructurados
    df.to_excel(f"informes/bajas_laliga_{fecha_hoy}.xlsx", index=False)
    df.to_csv(f"informes/bajas_laliga_{fecha_hoy}.csv", index=False, encoding='utf-8-sig')
    
    # Actualizar la portada del proyecto (README.md)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 📋 Informe Automatizado de Bajas de LaLiga\n\n")
        f.write(f"Última actualización de la plantilla de Primera División: **{fecha_hoy}**\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n*Nota: Los informes completos en Excel se almacenan cronológicamente dentro de la carpeta `informes/`.*")
        
    print(f"¡Base de datos ordenada y guardada con éxito! {len(datos)} registros cargados.")

if __name__ == "__main__":
    bajas_actuales = obtener_bajas_primera_division()
    guardar_reportes(bajas_actuales)
