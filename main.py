from notificador import NotificadorPrecios

def mostrar_productos(notifica):
    """Muestra la lista de prodcutos monitoreados"""
    productos = notifica.cargar_productos()

    if not productos:
        print("\nNo hay productos monitoreados")
        return
    
    print("\n=== PRODUCTOS MONITOREADOS ===")

    for i, producto in enumerate(productos, 1):
        print(f"\n{i}. {producto['nombre']}")
        print(f"   URL: {producto['url']}")
        print(f"   Precio actual: {producto.get('precio_actual', 'No disponible')}")
        print(f"   Precio deseado: {producto['precio_deseado']}")

        # Mostral historial de precios si existe
        if producto.get('historial_precios'):
            print("   Historial de precios recientes:")
            for registro in producto['historial_precios'][-3:]:   # Mostrar los ultimos 3 precios
                print(f"     {registro['fecha']}: {registro['precio']}")


def main():
    """Funcion principal con menu interactivo"""
    print("=== NOTIFICADOR DE PRECIO GENERICO ===")

    # Crear una instancia del notificador
    notifica = NotificadorPrecios()

    while True:
        print("\nOpciones:")
        print("1. Agregar un producto para monitorear")
        print("2. Mostrar productos monitoreados")
        print("3. Actualizar precios")
        print("4. Eliminar un producto")
        print("5. Salir")

        opcion = input("\nSeleciona una opcion (1-5):")

        if opcion == "1":
            # Agregar un producto
            nombre = input("\nIngresa el nombre del producto: ")
            url = input("\nIngresa la URL del producto: ")
            precio_deseado = float(input("Ingresa el precio deseado: "))

            usar_selector= input("Deseas especificar un selector CSS personalizado? (s/n) ").lower() == 's'
            selector_css = None

            if usar_selector:
                selector_css = input("Ingresa el selector CSS para el precio: ")

            # Preguntar por el separador de miles
            separador_miles = input("Cual es el separador de miles en el precio?. (. o ,) [por defecto ',']: ").strip()
            if separador_miles not in ['.', ',']:
                separador_miles = ','
                print("Usando separador de miles por defecto: ','")

            resultado = notifica.agregar_producto(nombre, url, precio_deseado, selector_css, separador_miles)

            if resultado:
                print(f"\nProducto '{nombre}' agregado correctamente")
            else:
                print(f"\nNo se pudo agregar el producto '{nombre}' (posiblemente ya existe)")

        elif opcion == "2":
            # Mostrar productos
            mostrar_productos(notifica)
        
        elif opcion == "3":
            # Actualiza precios
            print("\nActualizando precios de todos los productos...")
            productos_actualizados = notifica.actualizar_precios()

            if productos_actualizados:
                print(f"\n Se encontraron {len(productos_actualizados)} productos bajo el precio deseado!")
                for producto in productos_actualizados:
                    print(f"- {producto['nombre']}: Precio actual{['precio_actual']}")
            else:
                print("\nNo se encontraron cambios importantes en los precios")
        
        elif opcion == "4":
            # Elimina un producto
            mostrar_productos(notifica)

            productos = notifica.cargar_productos()
            if productos:
                try:
                    indice = int(input("\nIngresa el numero del producto a eliminar: "))
                    if notifica.eliminar_producto(indice):
                        print(f"\nProducto #{indice} eliminado correctamente")
                    else:
                        print(f"\nNo se pudo eliminar el producto #{indice}")
                except ValueError:
                    print("\nPor favor, ingresa un numero valido")
            else:
                print("\nNo hay productos para eliminar")

        elif opcion == "5":
            # Salir
            print("\nGracias por el usar el notificador de precios generico!")
            break

        else:
            print("\nOpcion no valida. Por favor, selecciona una opcion del 1 al 5.")

if __name__ == "__main__":
    main()