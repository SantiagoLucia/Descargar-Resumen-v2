from playwright.sync_api import sync_playwright
from configparser import ConfigParser
from pathlib import Path
import os

# Cargar configuración desde el archivo config.ini
config = ConfigParser()
config.read("config.ini")

# Variables de configuración
url = config["APP"]["URL"]
dni = config["APP"]["DNI"]
usr = config["APP"]["USR"]
pasw = config["APP"]["PASW"]
dir_desc = Path(config["APP"]["DIR_DESCARGA"])

# Constantes para selectores
DOC_NUMBER_SELECTOR = "//input[@id='loginFrm:docNumber']"
PASSWORD_SELECTOR = "//input[@id='loginFrm:password']"
NICKNAME_SELECTOR = "//input[@id='loginFrm:nickname']"
LOGIN_BUTTON_SELECTOR = "//input[@id='loginFrm:button']"
VIEW_SUMMARY_TEXT = "Ver Resumen"
DOWNLOAD_TEXT = "Descargar / Imprimir"

def main() -> None:
    """
    Función principal que automatiza el proceso de inicio de sesión y descarga de un archivo
    utilizando la biblioteca Playwright.
    """
    try:
        with sync_playwright() as pw:
            # Iniciar el navegador Chromium en modo headless
            browser = pw.chromium.launch(headless=True)
            # Crear un nuevo contexto de navegador con una ventana de 1280x720
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            # Abrir una nueva página en el contexto del navegador
            page = context.new_page()
            
            # Navegar a la URL especificada
            page.goto(url)
            # Rellenar los campos de inicio de sesión
            page.locator(DOC_NUMBER_SELECTOR).fill(dni)
            page.locator(PASSWORD_SELECTOR).fill(pasw)
            page.locator(NICKNAME_SELECTOR).fill(usr)
            # Hacer clic en el botón de inicio de sesión
            page.locator(LOGIN_BUTTON_SELECTOR).click()
            # Hacer clic en el enlace o botón "Ver Resumen"
            page.get_by_text(VIEW_SUMMARY_TEXT).click()
            
            # Esperar a que se inicie una descarga al hacer clic en "Descargar / Imprimir"
            with page.expect_download() as download_info:
                page.get_by_text(DOWNLOAD_TEXT).click()
            
            # Obtener la información de la descarga
            download = download_info.value
            filename = download.suggested_filename
            # Guardar el archivo descargado en el directorio especificado
            download.save_as(dir_desc / filename)
        
        # Abrir el archivo descargado con la aplicación predeterminada del sistema
        os.startfile(dir_desc / filename)
    except Exception as e:
        # Manejo de errores: imprimir el mensaje de error
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()