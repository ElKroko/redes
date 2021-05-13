'''Es el link entre el Cliente y el SC
Este nodo se encargara de realizar el seguimiento de las jugadas, y procesara las jugadas
para saber quien gano                                                                       '''

#Posibilidades de jugadas, un 90% de exito
# El primero que gana 3 rondas gana la partida.
# Puertos utiles: 49152 - 65535

### Funciones de Cachipun ###

def cachipun (jugada_cliente, jugada_servidor):     # Esta funcion siempre entrega resultado respecto a cliente
    jugadas = {
        "pi": [['pi', 'pa', 'ti'],[0, -1, 1]],      # Piedra
        "pa": [['pi', 'pa', 'ti'],[1, 0, -1]],      # Papel
        "ti": [['pi', 'pa', 'ti'],[-1, 1, 0]]}      # Tijera

    resultado = jugadas[jugada_cliente]

    for i in range(3):
        if jugada_servidor == resultado[0][i]:
            final = resultado[1][i]
            break
    
    return final

######### SOCKET #########

import socket as skt

HOST = "127.0.0.1"
TPORT = 65432
UPORT_SEND = 50000
UPORT_REC = 50001

BUFFER = 1024


print('Servidor TCP escuchando en: ', TPORT)

# Conexion TCP -> Cliente
with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as stcp:
    stcp.bind((HOST,TPORT))
    stcp.listen()
    conn_cli, addr_cli = stcp.accept()
    with conn_cli:
        print('Conectado por', addr_cli)
        send_stop = False

        while True:     # while de las solicitudes (TCP)
            solicitud_cliente = conn_cli.recv(BUFFER)
            print("Solicitud Cliente recibida")

            if solicitud_cliente.decode() == "STOP":
                send_stop = True
                

            # Mandar solicitud al UDP
            sudp_send = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
            print("Enviando solicitud via UDP a:", UPORT_SEND)
            if not send_stop:
                sudp_send.sendto("SOLICITAR".encode(), (HOST, UPORT_SEND))
            else:
                sudp_send.sendto("STOP".encode(), (HOST, UPORT_SEND))
                sudp_send.close()
                break
            
            
            # Recibir solicitud del UDP, si la solicitud esta correcta, Hacer puerto random
            with skt.socket(skt.AF_INET, skt.SOCK_DGRAM) as sudp_receive:
                sudp_receive.bind((HOST, UPORT_REC))
                puerto_random_udp, addr = sudp_receive.recvfrom(BUFFER)

                puerto_random_udp = puerto_random_udp.decode().strip().split(",")
                disponibilidad = puerto_random_udp[0]        
                puerto_random = puerto_random_udp[1]
            print("Resultado solicitud:")
            print("Disponibilidad: ", disponibilidad, "\tPuerto:", puerto_random)
            print()

            
            if disponibilidad > "2":
                conn_cli.send("Si".encode())     # Enviar resultado solicitud a TCP
                # Establecer nueva conexion UDP para jugar:
                if int(puerto_random) > 49152 and int(puerto_random) < 65535:

                    with skt.socket(skt.AF_INET, skt.SOCK_DGRAM) as sudp_juego:             # El resto del juego deberia transcurrir aqui...
                        sudp_juego.bind((HOST, int(puerto_random)))
                        print('\nLa partida transcurre en el puerto', puerto_random)
                        print()
                        print()

                        # Jugadas de cliente y servidor:
                        resultado = ['0','0','0']          # 3-lista de resultados, [puntaje_cliente, puntaje_servidor, ganador_ronda]
                        
                        ''' 
                            Procesar Turno
                        '''
                        
                        while int(resultado[0]) < 3 and int(resultado[1]) < 3:     
                            sudp_send.sendto("inicio".encode(), (HOST, UPORT_SEND))
                            # Espero jugada cliente 
                            jugada_cliente = conn_cli.recv(BUFFER).decode()

                            # Pedir jugada a UDP SC
                            jugada_SC, _ = sudp_juego.recvfrom(BUFFER)
                            jugada_servidor = jugada_SC.decode()
                            
                            

                            # Enviar jugada de servidor a cliente
                            conn_cli.sendall(jugada_servidor.encode())
                            _ = conn_cli.recv(BUFFER)

                            ''' 
                            Generar Resultados:
                            '''
                            resultado[2] = str(cachipun(jugada_cliente, jugada_servidor))

                            if resultado[2] == '1':   # Si cliente gana
                                resultado[0] = str(int(resultado[0]) + 1)
                            elif resultado[2] == '-1':   # Si servidor gana
                                resultado[1] = str(int(resultado[1]) + 1)

                            # Enviar resultados a Cliente
                            mensaje = ','.join(resultado)
                            conn_cli.send(mensaje.encode())
                        sudp_send.sendto("fin".encode(), (HOST, UPORT_SEND))
                        sudp_send.close()
            
            else:
                conn_cli.send("No".encode())     # Enviar resultado solicitud a TCP
                continue

# Replicar cierre de conexion a SC


print("Conexion TCP Cerrada...")
print('')
