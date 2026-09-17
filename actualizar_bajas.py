import requests
import pandas as pd
import datetime
import os

def extraer_bajas_api():
    # Obtener de forma segura la API Key desde los secretos de GitHub
    api_key = os.environ.get("API_FOOTBALL_KEY")
    
    if not api_key:
        print("Error: No se ha configurado la API Key en los secretos de GitHub.")
        return []

    url = "https://api-sports.io"
    
    # ID de LaLiga EA Sports = 140. Temporada actual obtenida dinámicamente.
    año_actual = datetime.datetime.now().year
    
    query_params = {
        "league": "140",
        "season": str(año_actual)
    }
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    try:
        response = requests.get(url, headers=headers, params=query_params, timeout=20)
        if response.status_code == 200:
            datos_json = response.json()
            lista_jugadores = datos_json.get("response", [])
            
            bajas_estructuradas = []
            for item in lista_jugadores:
                jugador = item.get("player", {})
                equipo = item.get("team", {})
                incidencia = item.get("injury", {})
                
                bajas_estructuradas.append({
                    "Equipo": equipo.get("name", "Desconocido"),
                    "Jugador": jugador.get("name", "Desconocido"),
                    "Tipo de Incidencia": "Médica / Sanción",
                    "Estado": incidencia.get("type", "Baja"),
                    "Detalle": incidencia.get("reason", "No especificado")
                })
            
            return bajas_estructuradas
        else:
            print(f"Error en API: Código de estado {response.status_code}")
            return []
    except Exception as e:
        print(f"Error de conexión con la API: {e}")
        return []

def guardar_reportes(datos):
    if not datos:
        print("No se encontraron bajas activas en la API para esta combinación de liga/año.")
        datos = [{"Equipo": "Sin datos", "Jugador": "N/A", "Tipo de Incidencia": "N/A", "Estado": "N/A", "Detalle": "API no devolvió registros"}]

    df = pd.DataFrame(datos)
    os.makedirs("informes", exist_ok=True)
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Guardar Excel y CSV en la carpeta informes/
    df.to_excel(f"informes/bajas_laliga_{fecha_hoy}.xlsx", index=False)
    df.to_csv(f"informes/bajas_laliga_{fecha_hoy}.csv", index=False, encoding='utf-8-sig')
    
    # Renderizar la portada README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 📋 Informe Automatizado de Bajas de LaLiga (API Real)\n\n")
        f.write(f"Última actualización mediante API-Football: **{fecha_hoy}**\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n*Los históricos se encuentran a salvo en la carpeta `informes/`.*")
    print(f"Archivos guardados con éxito para la fecha: {fecha_hoy}")

if __name__ == "__main__":
    datos_reales = extraer_bajas_api()
    guardar_reportes(datos_reales)
