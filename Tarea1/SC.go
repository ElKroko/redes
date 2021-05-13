// Bot o contrincante
// Generar jugadas aleatorias hasta que se le indique el final del juego
// Se conecta via UDP a el SI en el comienzo del juego, y tambien mediante UDP en cada partida pero en otro puerto (aleatorio)

package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"time"
)

// Retorna una jugada aleatoria
func jugada_cachi() string { 
	num_jugada := strconv.FormatInt(int64(rand.Intn(3)), 10)
	if num_jugada == "0"{
		return "pa"
		
	} else if num_jugada == "1"{
			return "pi"
			
	} else {
			return "ti"
	}
}

// Retorna un numero entre 1-10 para medir su disponibilidad, y un puerto aleatorio dentro de los recomendados
func rand_disp() string { 

	rand.Seed(time.Now().UnixNano())
	disponibilidad := strconv.FormatInt(int64(rand.Intn(10)), 10)
	puerto := strconv.FormatInt(int64((rand.Intn(16382)) + 49152), 10)
	fmt.Println("Disponibilidad Funcion: "+ disponibilidad + "\t Puerto Aleatorio: " + puerto)

	return disponibilidad + "," + puerto

}

func main() {

	IP := "localhost"
	PUERTO_REC := ":50000"
	PUERTO_SEND := ":50001"
	BUFFER := 1024
	
	fmt.Println("Iniciando Servidor Cachipun")

	// Establecer Conexion con puerto UDP fijo
	// En esta conexion, se debe preguntar por la disponibilidad
	s_rec, err := net.ResolveUDPAddr("udp4", IP+PUERTO_REC)
	conn_rec, err := net.ListenUDP("udp4",  s_rec)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Escuchando en" , s_rec)
	fmt.Println()
	
	for{
		//Recibir mensaje de SOLICITAR desde SI
		buffer := make([]byte, BUFFER)
		n, _, err := conn_rec.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println(err)
			return
		}

		if string(buffer[0:n]) == "SOLICITAR" {
			fmt.Println("Servidor Intermedio solicitando conexion en", s_rec)
			fmt.Println()

			// Establecer conexion en puerto 50001 y enviar resultado de solicitud
			
			s_send, err := net.ResolveUDPAddr("udp4", IP+PUERTO_SEND)
			conn_send, err := net.DialUDP("udp4", nil, s_send)
			if err != nil {
				fmt.Println(err)
				return
			}
			fmt.Println("Enviando respuesta a ", s_send)
			fmt.Println()

			// Preguntar x disponibilidad
			resultado_disponibilidad := rand_disp()
			data := []byte(resultado_disponibilidad)
			

			// Enviar puerto
			_, err2 := conn_send.Write(data)
			if err2 != nil{
				// handle error
				fmt.Println(err2)
				return
			}

			// Si la funcion rand_disp() entrega un valor admisible
			if resultado_disponibilidad[:1] > "2"{
				defer conn_send.Close()				// Se cierra la conexion con puerto :50001
				
				// Iniciar conexion UDP con el nuevo puerto random
				puerto_random := resultado_disponibilidad[2:]
				
				s_random, err := net.ResolveUDPAddr("udp4", IP+":"+puerto_random)
				conn_rand, err := net.DialUDP("udp4", nil, s_random)
				if err != nil{
					fmt.Println(err)
					return
				}

				fmt.Println("Enviando jugada a ", s_random)

				// Sincronizar con el "While de juego", donde transcurren los turnos
				buffer2 := make([]byte, BUFFER)
				n, _, err := conn_rec.ReadFromUDP(buffer2)
				if err != nil {
					fmt.Println(err)
					return
				}
				
				// Cada vez que se inicie una nueva iteracion, se espera que llegue "inicio"
				for string(buffer2[0:n]) == "inicio"{
					jugada := []byte(jugada_cachi())		// Se genera jugada aleatoria
					_, err := conn_rand.Write(jugada)		// Se envia jugada aleatoria a puerto random
					if err != nil{
						fmt.Println(err)
						return
					}
					buffer2 := make([]byte, BUFFER)			// Se vuelve a preguntar por la condicion del for.
					n, _, err := conn_rec.ReadFromUDP(buffer2)
					if err != nil {
						fmt.Println(err)
						return
					}
					
					if string(buffer2[0:n]) == "fin"{		// En caso de terminar juego, salir de este for para 
						defer conn_rand.Close()				// cerrar socket random
						break								// volver a pedir disponibilidad
					}
					
					if string(buffer2[0:n]) == "STOP"{		// Si se envia mensaje de cierre, 
						defer conn_rec.Close()				// cerrar socket :50000
						return
					}
				}
			}	
		} else if string(buffer[0:n]) == "STOP" {
			fmt.Println()
			fmt.Println("Tenemos que cerrar!!!")
			return
		}	
	}
}
