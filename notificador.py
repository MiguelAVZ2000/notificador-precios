import os
import json
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class NotificadorPrecios:
    def __init__(self, archivo_productos="productos_monitoreados.json"):
        self.archivo_productos = archivo_productos

    def obtener_precio(self, url, selector_css=None, separador_miles=','):
        """Extrae el precio de un producto desde cualquier sitio web"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
            }

            respuesta = requests.get(url, headers=headers, timeout=10)

            if respuesta.status_code != 200:
                return None

            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar el precio con el selector proporcionado o con selectores comunes
            precio_elem = None
            if selector_css:
                precio_elem = soup.select_one(selector_css)
            else:
                selectores_comunes = [
                    '.price', '.product-price', '.offer-price', '.current-price',
                    '[itemprop="price"]', '.price-value', '.price-current',
                    '.a-price .a-offscreen', '#priceblock_ourprice', '#priceblock_dealprice',
                    '.andes-money-amount__fraction'
                ]

                for selector in selectores_comunes:
                    precio_elem = soup.select_one(selector)
                    if precio_elem:
                        break

            if not precio_elem:
                return None

            precio_texto = precio_elem.text.strip()

            # Ajustar separador de miles
            if separador_miles == '.':
                precio_texto = precio_texto.replace('.', '').replace(',', '.')
            else:
                precio_texto = precio_texto.replace(',', '')

            # Extraer número
            precio_limpio = re.sub(r'[^\d.]', '', precio_texto)
            match = re.search(r'\d+\.\d+|\d+', precio_limpio)

            return float(match.group()) if match else None

        except Exception as e:
            print(f"Error en obtener_precio: {e}")
            return None

    def cargar_productos(self):
        """Carga la lista de productos monitoreados desde el archivo"""
        if os.path.exists(self.archivo_productos):
            try:
                with open(self.archivo_productos, 'r', encoding='utf-8') as archivo:
                    productos = json.load(archivo)
                    print(f"Productos cargados: {productos}")  # Depuración
                    return productos
            except Exception as e:
                print(f"Error al cargar productos: {e}")
        return []

    def guardar_productos(self, productos):
        """Guarda la lista de productos en el archivo JSON"""
        try:
            with open(self.archivo_productos, 'w', encoding='utf-8') as archivo:
                json.dump(productos, archivo, indent=4, ensure_ascii=False)
                print(f"Productos guardados correctamente: {productos}")  # Depuración
        except Exception as e:
            print(f"Error al guardar productos: {e}")

    def agregar_producto(self, nombre, url, precio_deseado, selector_css=None, separador_miles=','):
        """Agrega un nuevo producto a la lista de monitoreados"""
        productos = self.cargar_productos()

        # Verificar si el producto ya existe
        for producto in productos:
            if producto['url'] == url:
                print("El producto ya existe, no se agregará.")
                return False  # No agregar duplicados

        # Obtener el precio actual
        precio_actual = self.obtener_precio(url, selector_css, separador_miles)
        print(f"Precio obtenido para {nombre}: {precio_actual}")  # Depuración
        # Crear el nuevo producto
        nuevo_producto = {
            'nombre': nombre,
            'url': url,
            'precio_deseado': precio_deseado,
            'precio_actual': precio_actual,
            'selector_css': selector_css,
            'separador_miles': separador_miles,
            'fecha_agregado': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'historial_precios': []
        }

        if precio_actual is not None:
            nuevo_producto['historial_precios'].append({
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'precio': precio_actual
            })

        productos.append(nuevo_producto)
        
        self.guardar_productos(productos)  # Guardar en JSON
        print(f"Producto agregado: {nuevo_producto}")  # Depuración
        return True

    def actualizar_precios(self):
        """Actualiza los precios de todos los productos monitoreados"""
        productos = self.cargar_productos()
        productos_actualizados = []

        for producto in productos:
            separador_miles = producto.get('separador_miles', ',')
            precio_actual = self.obtener_precio(producto['url'], producto.get('selector_css'), separador_miles)

            if precio_actual is not None:
                producto['precio_actual'] = precio_actual

                # Agregar al historial
                producto['historial_precios'].append({
                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'precio': precio_actual
                })

                # Limitar el historial a los últimos 30 registros
                if len(producto['historial_precios']) > 30:
                    producto['historial_precios'] = producto['historial_precios'][-30:]

                # Verificar si el precio ha bajado o alcanzado el precio deseado
                if precio_actual <= producto['precio_deseado']:
                    productos_actualizados.append(producto)

        # Guardar los productos después de actualizar todos
        self.guardar_productos(productos)

        return productos_actualizados

    def eliminar_producto(self, indice):
        """Elimina un producto de la lista de monitoreados"""
        productos = self.cargar_productos()

        if not productos or indice < 1 or indice > len(productos):
            print("Índice fuera de rango o lista vacía.")
            return False

        producto_eliminado = productos.pop(indice - 1)
        self.guardar_productos(productos)

        print(f"Producto eliminado: {producto_eliminado}")
        return True
