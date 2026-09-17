import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

def scraping_futbol_fantasy():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    lista_bajas = []

    # 1. PROCESAR LESIONADOS Y DUDAS
    url_lesionados = "https://www.futbolfantasy.com/laliga/lesionados"
    res_les = requests.get(url_lesionados, headers=headers)
    
    if res_les.status_code == 200:
        soup = BeautifulSoup(res_les.text, 'html.parser')
        # Buscamos los bloques de cada equipo
        bloques_equipos = soup.find_all('div', class_='box-tabla-equipo')
        
        for bloque in bloques_equipos:
            # Obtener el nombre del equipo
            nombre_equipo = bloque.find('h2').text.strip() if bloque.find('h2') else "Desconocido"
            
            # Buscar los jugadores dentro de las filas/listas de ese equipo
            jugadores_bajas = bloque.find_all('tr', class_=['baja', 'duda', 'alta'])
            for j in jugadores_bajas:
                clases = j.get('class', [])
                estado = "Baja" if "baja" in clases else ("Duda" if "duda" in clases else "Alta/Disponible")
                
                nombre_jugador = j.find('span', class_='nombre').text.strip() if j.find('span', class_='nombre') else "Desconocido"
                motivo = j.find('td', class_='motivo').text.strip() if j.find('td', class_='motivo') else "No especificado"
                
                lista_bajas.append({
                    "Equipo": nombre_equipo,
                    "Jugador": nombre_jugador,
                    "Tipo de Incidencia": "Física / Médica",
                    "Estado": estado,
                    "Detalle": motivo
                })

    # 2. PROCESAR SANCIONADOS (TARJETAS / SANCIONES DISCIPLINARIAS)
    url_sancionados = "https://futbolfantasy.com"
    res_san = requests.get(url_sancionados, headers=headers)
    
    if res_san.status_code == 200:
        soup_san = BeautifulSoup(res_san.text, 'html.parser')
        bloques_equipos_san = soup_san.find_all('div', class_='box-tabla-equipo')
        
        for bloque in bloques_equipos_san:
            nombre_equipo = bloque.find('h2').text.strip() if bloque.find('h2') else "Desconocido"
            
            jugadores_sancionados = bloque.find_all('tr', class_='baja')
            for j in jugadores_sancionados:
                nombre_jugador = j.find('span', class_='nombre').text.strip() if j.find('span', class_='nombre') else "Desconocido"
                motivo = j.find('td', class_='motivo').text.strip() if j.find('td', class_='motivo') else "Sanción por tarjetas"
                
                lista_bajas.append({
                    "Equipo": nombre_equipo,
                    "Jugador": nombre_jugador,
                    "Tipo de Incidencia": "Disciplinaria (Sanción)",
                    "Estado": "Baja",
                    "Detalle": motivo
                })

    return lista_bajas

def guardar_reportes(datos):
    if not datos:
        print("No se pudieron recopilar datos.")
        return

    df = pd.DataFrame(datos)
    
    # Crear carpetas si no existen
    os.makedirs("informes", exist_ok=True)
    
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Guardar archivo Excel interactivo y CSV histórico
    archivo_excel = f"informes/bajas_laliga_{fecha_hoy}.xlsx"
    archivo_csv = f"informes/bajas_laliga_{fecha_hoy}.csv"
    
    df.to_excel(archivo_excel, index=False)
    df.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
    
    # Generar tabla bonita en el archivo de portada (README.md)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 📋 Informe Automatizado de Bajas de LaLiga\n\n")
        f.write(f"Última actualización automática: **{fecha_hoy}**\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n*Los archivos Excel y CSV completos se encuentran guardados en la carpeta `informes/`.*")
        
    print(f"Archivos guardados correctamente para la fecha: {fecha_hoy}")

if __name__ == "__main__":
    datos_extraidos = scraping_futbol_fantasy()
    guardar_reportes(datos_extraidos)
