import requests
import json

API_KEY = "77527916-4236-4277-8d73-c179d496e577"

def obtener_coordenadas(ciudad, pais):
    url_geo = f"https://graphhopper.com/api/1/geocode?q={ciudad},{pais}&locale=es&key={API_KEY}"
    try:
        respuesta = requests.get(url_geo).json()
        if respuesta.get("hits"):
            point = respuesta["hits"][0]["point"]
            return point["lat"], point["lng"], respuesta["hits"][0]["name"]
    except Exception as e:
        print(f"Error al conectar con el servicio de mapas: {e}")
    return None

def calcular_ruta():
    while True:
        print("\n=============================================")
        print(" SISTEMA DE MEDICIÓN DE VIAJES: CHILE - PERÚ ")
        print("=============================================")
        print("(Presione 's' en cualquier momento para salir)")
        
        # 1. Solicitar Ciudad de Origen (Chile)
        origen_input = input("Ingrese Ciudad de Origen (en Chile): ").strip()
        if origen_input.lower() == 's': break
        
        # 2. Solicitar Ciudad de Destino (Perú)
        destino_input = input("Ingrese Ciudad de Destino (en Perú): ").strip()
        if destino_input.lower() == 's': break
        
        print("\nBuscando localizaciones...")
        coord_origen = obtener_coordenadas(origen_input, "Chile")
        coord_destino = obtener_coordenadas(destino_input, "Peru")
        
        if not coord_origen or not coord_destino:
            print("No se encontraron una o ambas ciudades. Intente nuevamente.")
            continue
            
        lat_ori, lon_ori, nombre_ori = coord_origen
        lat_des, lon_des, nombre_des = coord_destino
        
        # 3. Seleccionar Medio de Transporte
        print("\nSeleccione el Medio de Transporte:")
        print("1. Automóvil (car)")
        print("2. Bicicleta (bike)")
        print("3. A pie (foot)")
        opcion = input("Elija una opción (1-3) o 's' para salir: ").strip()
        
        if opcion.lower() == 's': break
        elif opcion == '1': vehiculo = "car"
        elif opcion == '2': vehiculo = "bike"
        elif opcion == '3': vehiculo = "foot"
        else:
            print("Opción inválida, usando Automóvil por defecto.")
            vehiculo = "car"
            
        print(f"\nCalculando ruta desde {nombre_ori} hasta {nombre_des} en {vehiculo}...")
        
        # Consulta de enrutamiento a la API de Graphhopper
        url_route = f"https://graphhopper.com/api/1/route?point={lat_ori},{lon_ori}&point={lat_des},{lon_des}&vehicle={vehiculo}&locale=es&instructions=true&key={API_KEY}"
        
        try:
            res_route = requests.get(url_route).json()
            if "paths" in res_route:
                ruta = res_route["paths"][0]
                
                # Conversión de unidades obligatorias
                distancia_km = ruta["distance"] / 1000
                distancia_mi = distancia_km * 0.621371
                
                # Conversión de tiempo (de milisegundos a horas/minutos)
                tiempo_seg = ruta["time"] / 1000
                horas = int(tiempo_seg // 3600)
                minutos = int((tiempo_seg % 3600) // 60)
                
                # Mostrar resultados principales
                print("\n---------------- RESULTADOS ----------------")
                print(f"Ruta: {nombre_ori} -> {nombre_des}")
                print(f"Distancia en Kilómetros: {distancia_km:.2f} km")
                print(f"Distancia en Millas: {distancia_mi:.2f} mi")
                print(f"Duración estimada: {horas} horas y {minutos} minutos")
                print("--------------------------------------------")
                
                # 4. Narrativa del Viaje (Instrucciones paso a paso)
                print("\nNARRATIVA DEL VIAJE (Indicaciones de ruta):")
                for paso in ruta["instructions"]:
                    texto = paso["text"]
                    dist_paso = paso["distance"] / 1000
                    print(f"- {texto} ({dist_paso:.2f} km)")
                    
            else:
                print("No se pudo trazar una ruta terrestre continua entre estas ciudades con el transporte seleccionado.")
        except Exception as e:
            print(f"Error al calcular la ruta: {e}")
            
        # Pausa para poder leer los datos antes del siguiente ciclo
        input("\nPresione Enter para realizar otra consulta...")

    print("\nGracias por usar el sistema de medición. ¡Saliendo!")

if __name__ == "__main__":
    calcular_ruta()
