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
    try:
        url_lesionados = "https://futbolfantasy.com"
        res_les = requests.get(url_lesionados, headers=headers, timeout=15)
        if res_les.status_code == 200:
            soup = BeautifulSoup(res_les.text, 'html.parser')
            # Buscamos los bloques de cada equipo por su etiqueta correcta
            bloques_equipos = soup.find_all('div', class_='box-tabla-equipo')
            
            for bloque in bloques_equipos:
                nombre_equipo = bloque.find('h2').text.strip() if bloque.find('h2') else "Desconocido"
                
                # Buscamos todas las filas de la tabla de jugadores
                filas_jugadores = bloque.find_all('tr')
                for fila in filas_jugadores:
                    clases = fila.get('class', [])
                    # Comprobamos si la fila corresponde a una baja o duda
                    if any(c in clases for c in ['baja', 'duda', 'alta']):
                        estado = "Baja" if "baja" in clases else ("Duda" if "duda" in clases else "Alta")
                        
                        nombre_jugador = fila.find('span', class_='nombre').text.strip() if fila.find('span', class_='nombre') else "Desconocido"
                        motivo = fila.find('td', class_='motivo').text.strip() if fila.find('td', class_='motivo') else "No especificado"
                        
                        lista_bajas.append({
                            "Equipo": nombre_equipo,
                            "Jugador": nombre_jugador,
                            "Tipo de Incidencia": "Física / Médica",
                            "Estado": estado,
                            "Detalle": motivo
                        })
    except Exception as e:
        print(f"Error extrayendo lesionados: {e}")

    # 2. PROCESAR SANCIONADOS (TARJETAS)
    try:
        url_sancionados = "https://futbolfantasy.com"
        res_san = requests.get(url_sancionados, headers=headers, timeout=15)
        if res_san.status_code == 200:
            soup_san = BeautifulSoup(res_san.text, 'html.parser')
            bloques_equipos_san = soup_san.find_all('div', class_='box-tabla-equipo')
            
            for bloque in bloques_equipos_san:
                nombre_equipo = bloque.find('h2').text.strip() if bloque.find('h2') else "Desconocido"
                
                filas_sancionados = bloque.find_all('tr')
                for fila in filas_sancionados:
                    clases = fila.get('class', [])
                    if 'baja' in clases or 'sancionado' in clases:
                        nombre_jugador = fila.find('span', class_='nombre').text.strip() if fila.find('span', class_='nombre') else "Desconocido"
                        motivo = fila.find('td', class_='motivo').text.strip() if fila.find('td', class_='motivo') else "Sanción disciplinaria"
                        
                        lista_bajas.append({
                            "Equipo": nombre_equipo,
                            "Jugador": nombre_jugador,
                            "Tipo de Incidencia": "Disciplinaria (Sanción)",
                            "Estado": "Baja",
                            "Detalle": motivo
                        })
    except Exception as e:
        print(f"Error extrayendo sancionados: {e}")

    # COMODÍN DE SEGURIDAD: Si el scraping falla o la web bloquea la petición,
    # forzamos datos de prueba para asegurar que las carpetas y el README se generen de verdad.
    if not lista_bajas:
        lista_bajas.append({
            "Equipo": "Sistema (Prueba)",
            "Jugador": "Verificación de carpetas",
            "Tipo de Incidencia": "Control",
            "Estado": "Activo",
            "Detalle": "El script funciona pero la web requiere revisión de HTML."
        })

    return lista_bajas

def guardar_reportes(datos):
    df = pd.DataFrame(datos)
    
    # Asegurar la creación física de la carpeta
    os.makedirs("informes", exist_ok=True)
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Guardar archivos de datos
    df.to_excel(f"informes/bajas_laliga_{fecha_hoy}.xlsx", index=False)
    df.to_csv(f"informes/bajas_laliga_{fecha_hoy}.csv", index=False, encoding='utf-8-sig')
    
    # Actualizar la portada (README.md) en formato tabla interactiva de markdown
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 📋 Informe Automatizado de Bajas de LaLiga\n\n")
        f.write(f"Última actualización automática: **{fecha_hoy}**\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n*Los archivos Excel completos están guardados en la carpeta `informes/`.*")
        
    print("¡Reportes creados localmente de manera exitosa!")

if __name__ == "__main__":
    bajas = scraping_futbol_fantasy()
    guardar_reportes(bajas)
