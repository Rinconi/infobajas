import requests
import pandas as pd
import datetime
import os
import time

def extraer_bajas_por_equipos():
    api_key = os.environ.get("API_FOOTBALL_KEY")
    if not api_key:
        print("Error: No se ha configurado la API Key.")
        return []

    url = "https://api-sports.io"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    # Diccionario con los IDs oficiales de API-Football para los equipos de LaLiga
    equipos_laliga = {
        529: "FC Barcelona", 530: "Atletico Madrid", 541: "Real Madrid",
        531: "Athletic Club", 532: "Valencia", 533: "Villarreal", 
        536: "Sevilla", 537: "Las Palmas", 538: "Celta Vigo", 
        543: "Real Betis", 546: "Getafe", 547: "Girona", 
        548: "Real Sociedad", 720: "Valladolid", 726: "Leganes",
        727: "Osasuna", 728: "Rayo Vallecano", 732: "Alaves", 
        794: "Espanyol", 968: "Mallorca"
    }

    bajas_totales = []
    año_actual = str(datetime.datetime.now().year)

    print("Iniciando la descarga de bajas equipo por equipo...")
    
    for id_equipo, nombre_espanol in equipos_laliga.items():
        query_params = {
            "team": str(id_equipo),
            "season": año_actual
        }
        
        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=15)
            if response.status_code == 200:
                datos = response.json().get("response", [])
                
                for item in datos:
                    jugador = item.get("player", {})
                    incidencia = item.get("injury", {})
                    
                    # Filtrar si no es una baja real o si carece de datos válidos
                    if not jugador.get("name"):
                        continue
                        
                    bajas_totales.append({
                        "Equipo": nombre_espanol,
                        "Jugador": jugador.get("name"),
                        "Tipo de Incidencia": incidencia.get("type", "Médica / Sanción"),
                        "Estado": "Baja",
                        "Detalle": incidencia.get("reason", "No especificado")
                    })
            
            # Pausa de seguridad para respetar el límite de peticiones del plan gratuito
            time.sleep(1)
            
        except Exception as e:
            print(f"Error con el equipo {nombre_espanol}: {e}")

    return bajas_totales

def guardar_reportes(datos):
    if not datos:
        print("No hay bajas reportadas actualmente en la API.")
        datos = [{"Equipo": "Sin bajas", "Jugador": "Ninguno", "Tipo de Incidencia": "N/A", "Estado": "N/A", "Detalle": "Todos los planteles limpios"}]

    df = pd.DataFrame(datos)
    os.makedirs("informes", exist_ok=True)
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Guardar los archivos físicos
    df.to_excel(f"informes/bajas_laliga_{fecha_hoy}.xlsx", index=False)
    df.to_csv(f"informes/bajas_laliga_{fecha_hoy}.csv", index=False, encoding='utf-8-sig')
    
    # Reescribir la portada del proyecto
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 📋 Informe Automatizado de Bajas de LaLiga\n\n")
        f.write(f"Última actualización por escaneo de equipos: **{fecha_hoy}**\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n*Los históricos en Excel se guardan automáticamente en la carpeta `informes/`.*")
    print(f"¡Proceso finalizado con éxito! {len(datos)} registros procesados.")

if __name__ == "__main__":
    datos_reales = extraer_bajas_por_equipos()
    guardar_reportes(datos_reales)
