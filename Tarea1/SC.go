// Bot o contrincante
// Generara jugadas aleatorias hasta que se le indique el final del juego
// Se conecta via UDP a el SI en el comienzo del juego, y tambien mediante UDP en cada partida pero en otro puerto (aleatorio)

// Averiguar disponibilidad del servidor cachipun: puedo jugar? (Esta respuesta debe ser si o no, los ayudantes sugieren un 90% exito.)

package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"time"
)


func jugada_cachi() string { // Retorna un numero valido como puerto, o 0
	//rand.Seed(time.Now().UnixNano())
	num_jugada := strconv.FormatInt(int64(rand.Intn(3)), 10)
	if num_jugada == "0"{
		return "pa"
		
	} else if num_jugada == "1"{
			return "pi"
			
	} else {
			return "ti"
	}
}


func rand_disp() string { // Retorna un numero valido como puerto, o 0

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

	fmt.Println(" Escuchando en" , s_rec)
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
			
			resultado_disponibilidad := rand_disp()
			data := []byte(resultado_disponibilidad)
			// Preguntar x disponibilidad

			// Enviar puerto
			_, err2 := conn_send.Write(data)

			if err2 != nil{
				// handle error
				fmt.Println(err2)
				return
			}
			if resultado_disponibilidad[:1] > "2"{
				defer conn_send.Close()
				// Iniciar conexion UDP con el nuevo puerto random
				puerto_random := resultado_disponibilidad[2:]
				
				s_random, err := net.ResolveUDPAddr("udp4", IP+":"+puerto_random)
				conn_rand, err := net.DialUDP("udp4", nil, s_random)
				if err != nil{
					fmt.Println(err)
					return
				}

				fmt.Println("Enviando jugada a ", s_random)
				// While de resultados, SI envia "inicio" cuando comienza y "fin" cuando termina
				buffer2 := make([]byte, BUFFER)
				n, _, err := conn_rec.ReadFromUDP(buffer2)
				if err != nil {
					fmt.Println(err)
					return
				}
				
				for string(buffer2[0:n]) == "inicio"{
					//fmt.Println("Recibi inicio")
					jugada := []byte(jugada_cachi())
					_, err := conn_rand.Write(jugada)
					if err != nil{
						fmt.Println(err)
						return
					}
					buffer := make([]byte, BUFFER)
					n, _, err := conn_rec.ReadFromUDP(buffer)
					if err != nil {
						fmt.Println(err)
						return
					}

					if string(buffer[0:n]) == "STOP"{
						return
					}
				}
			}
			
			
			
			

			




		} else if string(buffer[0:n]) == "STOP" {
			fmt.Println()
			fmt.Println("Tenemos que cerrar!!!")
			return
		}

	

		//_, err := conn_send.WriteToUDP([])

		
	}
	

	
	
		//cerrar conexion si no hay uwu
	

	


	// Cerrar conexion UDP puerto fijo

	// Establecer conexion con SI en nuevo puerto


	
	// For
		// Recibir peticion jugada


		// Hacer una jugada random



		// enviar jugada random


	// Cerrar conexion cuando indique SI

}
