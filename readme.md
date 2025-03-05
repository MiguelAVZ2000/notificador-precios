# Notificador de Precios

Este es un script en Python que monitorea los precios de productos en línea y envía notificaciones cuando los precios bajan o alcanzan un valor deseado.

## 🚀 Características

- Extrae precios de productos de sitios web automáticamente.
- Soporte para múltiples tiendas en línea.
- Guarda el historial de precios de cada producto.
- Funciona con `requests`, `BeautifulSoup` y `Selenium` (para sitios dinámicos).

## 📦 Requisitos

Asegúrate de tener Python 3 instalado y las siguientes dependencias:

Instalación y Uso
Clonar el repositorio:


git clone https://github.com/MiguelAVZ2000/notificador-precios.git
cd notificador-precios
Crear un entorno virtual (opcional, pero recomendado):


python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
Instalar dependencias:


pip install -r requirements.txt
Ejecutar el script:


python main.py


Configuración
Puedes modificar productos_monitoreados.json para agregar productos manualmente o usar el script para añadirlos automáticamente.


