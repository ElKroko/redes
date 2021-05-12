# En la version basica, debemos jugar cachipun contra un bot.

# Se comunica mediante TCP con el SI
# Pedir jugadas, mostrar resultados por ronda y por partida

# Cliente envia señal STOP, y se terminan en paralelo los 3 procesos.

# Los resultados se muestran en el cliente, pero la logica es en SI


import socket

HOST = "127.0.0.1"
PORT = 65432

BUFFER = 1024

jugadas = {1: "pi", 2: "pa", 3: "ti"}


print("--------- Interfaz del CLIENTE ---------")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    flag = True
    while flag:     #   while de disponibilidadavde jugar
        # Solicitar inicio de partida
        s.send("SOLICITAR INICIO".encode())         # Solicitar juego
        respuesta_solicitud = int(s.recv(BUFFER).decode())        # Esperar respuesta del Servidor

        if respuesta_solicitud:   
            print('')
            print("Hola, esto cachipun. Juegue..")      
                        
            resultado = [0,0]          # 2-lista de resultados
            while resultado[0] < 3 and resultado[1] < 3:     #   while de jugada hasta 3 ptos
                #       Hacer Jugada

                while True:
                    print("\nSelecciona una de las siguientes opciones: \n 1: piedra \t 2: papel \t 3: tijera ")
                    opcion = int(input(">> ")) 
                    try:
                        opcion = jugadas[opcion]
                        break
                    except:
                        print("Seleccione una opcion valida!")

                print("\n[*] Usted jugo ", opcion)
                s.send(opcion.encode())

                #       Recibe Resultado jugada

                recibe_jugada = s.recv(BUFFER)
                print("[*] El Bot jugo ",  recibe_jugada.decode())
                print("---")

                s.send("OK".encode())


                recibe_resultado = s.recv(BUFFER).decode().split(",")
                
                # condiciones while de jugada x ahora
                if recibe_resultado[2] == '1':
                    resultado[0] += 1
                elif recibe_resultado[2] == '-1':
                    resultado[1] += 1

                dicc_resultados = {-1: "servidor", 0:"nadie", 1:"usted"}
                print("[*] El ganador de esta ronda fue \t", dicc_resultados[int(recibe_resultado[2])])
                print("[*] El marcador actual es Jugador: "+ recibe_resultado[0]+", Bot: "+ recibe_resultado[1])


            if resultado[0] == 3: 
                print("\n[*] El ganador de la partida fue: Jugador")
            elif resultado[1] == 3:
                print("\n[*] El ganador de la partida fue: Servidor")

            
            
            #       Despues de que uno gane  -> Esperar siguiente juego
            seguir_jugando = int(input("\nDesea seguir jugando?\n(1) Si \t (0) No\n>> "))
        
            if seguir_jugando:
                continue
            else:
                # Decirle al servidor que cierre
                    # Al cerrar la conexion, el servidor automaticamente se cierra.
                break

        else:
            print("El servidor cachipun no esta disponible...")
            flag = False

print("\nCerrando Conexion")