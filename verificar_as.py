def verificar_as():
    print("--- Verificador de Sistema Autónomo (AS) BGP ---")
    entrada = input("Ingrese el número de AS de BGP (o 's' para salir): ")

    if entrada.lower() == 's':
        print("Saliendo del programa.")
        return

    try:
        num_as = int(entrada)

        # Validación de rangos privados estándar
        if (64512 <= num_as <= 65534) or (4200000000 <= num_as <= 4294967294):
            print(f"El número de AS {num_as} corresponde a un rango PRIVADO.")
        elif num_as <= 0 or num_as == 65535 or num_as > 4294967295:
            print(f"El número de AS {num_as} es un valor RESERVADO o INVÁLIDO.")
        else:
            print(f"El número de AS {num_as} corresponde a un rango PÚBLICO.")

    except ValueError:
        print("Error: Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    verificar_as()
