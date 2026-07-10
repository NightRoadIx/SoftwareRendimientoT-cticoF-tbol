from firebase import firebase

# Inicializa la aplicación de Firebase
firebase = firebase.FirebaseApplication("https://trabajoterminal-c-default-rtdb.firebaseio.com/", None)

# Estructura de evaluaciones con todas las variables a actualizar
estructura_evaluaciones = {
    'Oscar': {
        'pases_acertados': '24/45',
        'porcentaje_pases': 53,
        'tiros_acertados': '0/0',
        'porcentaje_tiros': 0,
        'posicionamiento': '84%',
        'porcentaje_posicion': 84,
        'calificacion': 6.7
    },
    'Carlos': {
        'pases_acertados': '5/8',
        'porcentaje_pases': 62.5,
        'tiros_acertados': '6/6',
        'porcentaje_tiros': 100,
        'posicionamiento': '62.5%',
        'porcentaje_posicion': 62.5,
        'calificacion': 7.75
    },
    'Santander': {
        'pases_acertados': '28/45',
        'porcentaje_pases': 70,
        'tiros_acertados': '0/0',
        'porcentaje_tiros': 0,
        'posicionamiento': '90%',
        'porcentaje_posicion': 90,
        'calificacion': 6.0
    }
}

# Función para actualizar datos en Firebase desde estructura_evaluaciones
def actualizar_datos(datos_actualizados):
    if datos_actualizados:
        for persona, variables in datos_actualizados.items():
            # Subir el valor a Firebase para cada variable de la persona
            for variable, valor in variables.items():
                result = firebase.put(f'/Evaluaciones/{persona}', variable, valor)
                if result:
                    print(f"Valor '{variable}' de '{persona}' actualizado exitosamente en Firebase")
                else:
                    print(f"Error al actualizar valor '{variable}' de '{persona}' en Firebase")
    else:
        print("No hay datos para actualizar en Firebase.")

# Llamar a la función para actualizar los datos en Firebase
actualizar_datos(estructura_evaluaciones)
