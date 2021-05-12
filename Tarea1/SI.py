'''Es el link entre el Cliente y el SC
Este nodo se encargara de realizar el seguimiento de las jugadas, y procesara las jugadas
para saber quien gano
'''

# Averiguar disponibilidad del servidor cachipun: puedo jugar? (Esta respuesta debe ser si o no, los ayudantes sugieren un 90% exito.)

# El primero que gana 3 rondas gana la partida.


# Puertos utiles: 49152 - 65535

### Funciones de Cachipun ###



def cachipun (jugada_cliente, jugada_servidor):                 # Esta funcion siempre entrega resultado respecto a cliente
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
UPORT = 50000

BUFFER = 1024

# Conexion TCP -> Cliente

print('Servidor TCP escuchando en: ', TPORT)


with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as stcp:
    stcp.bind((HOST,TPORT))
    stcp.listen()
    conn_cli, addr_cli = stcp.accept()
    with conn_cli:
        print('Conectado por', addr_cli)
        while True:     # while de las solicitudes (TCP)
            solicitud_cliente = conn_cli.recv(BUFFER)

            # Mandar solicitud al UDP
            with skt.socket(skt.AF_INET, skt.SOCK_DGRAM) as sudp:
                sudp.bind((HOST, UPORT))
                print("Preguntando a Servidor UDP en puerto", UPORT, "si esta disponible...")
                sudp.sendto("SOLICITAR".encode(), (HOST, UPORT))
                puerto_random_udp = sudp.recv(BUFFER)            # Recibir solicitud del UDP, si la solicitud esta correcta, Hacer puerto random

            # Establecer nueva conexion UDP para jugar:
            if int(puerto_random_udp) > 49152 and int(puerto_random_udp) < 65535:
                with skt.socket(skt.AF_INET, skt.SOCK_DGRAM) as sudp_juego:             # El resto del juego deberia transcurrir aqui...
                    sudp_juego.bind((HOST, puerto_random_udp))
                    print('La partida transcurre en el puerto,', puerto_random_udp,'de SC')

                    conn_cli.send("1".encode())     # Enviar resultado solicitud a TCP

                    # Jugadas de cliente y servidor:
                    resultado = ['0','0','0']          # 3-lista de resultados, [puntaje_cliente, puntaje_servidor, ganador_ronda]
                    while int(resultado[0]) < 3 and int(resultado[1]) < 3:     # while de las jugadas

                        # Espero jugada cliente 
                        jugada_cliente = conn_cli.recv(BUFFER).decode()

                        # Pedir jugada a UDP

                        # Recibir jugada UDP
                        jugada_servidor = "pa"

                        # Enviar jugada de servidor a cliente
                        conn_cli.sendall(jugada_servidor.encode())
                        _ = conn_cli.recv(BUFFER)

                        # Enviar resultados de jugadas
                        resultado[2] = str(cachipun(jugada_cliente, jugada_servidor))

                        if resultado[2] == '1':   # Si cliente gana
                            resultado[0] = str(int(resultado[0]) + 1)
                        elif resultado[2] == '-1':   # Si servidor gana
                            resultado[1] = str(int(resultado[1]) + 1)

                        
                        mensaje = ','.join(resultado)
                        conn_cli.send(mensaje.encode())
                

                    



            '''
            print('Recibido cliente: ', repr(data))
            if not data:
                break
            conn.sendall(data)
            '''

print("Conexion TCP Cerrada...")
print('')






# Conexion UDP -> Servidor Cachipun

with skt.socket(skt.AF_INET, skt.SOCK_DGRAM) as sudp:
    sudp.bind((HOST, UPORT))
    print("Servidor UDP escuchando en puerto: ", UPORT)

    msg, clientAddr = sudp.recvfrom(BUFFER)
    message = msg.decode()
    print("(X) Se recibe: ", message)
    response = str('El largo de ' + message.strip()+ ' es de ' + str(len(message)) + ' letras')
    sudp.sendto(response.encode(), clientAddr)