// Bot o contrincante
// Generara jugadas aleatorias hasta que se le indique el final del juego
// Se conecta via UDP a el SI en el comienzo del juego, y tambien mediante UDP en cada partida pero en otro puerto (aleatorio)

// Averiguar disponibilidad del servidor cachipun: puedo jugar? (Esta respuesta debe ser si o no, los ayudantes sugieren un 90% exito.)

package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
	IP := "localhost"
	PUERTO := ":50000"
	BUFFER := 1024
	s, err := net.ResolveUDPAddr("udp4", IP+PUERTO)
	c, err := net.DialUDP("udp4", nil, s)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Printf("El servidor UDP es %s\n", c.RemoteAddr().String())

	for {
		// Se escribe por consola el mensaje a enviar
		reader := bufio.NewReader(os.Stdin)
		fmt.Print(">> ")
		text, _ := reader.ReadString('\n')

		// Se codifica en bytes para el buffer
		data := []byte(text)

		// Se envia el mensaje
		_, err = c.Write(data)

		if strings.TrimSpace(string(data)) == "STOP" {
			fmt.Println("Finalizando Conexion...")
			return
		}

		if err != nil {
			fmt.Println(err)
			return
		}

		buffer := make([]byte, BUFFER)
		n, _, err := c.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println(err)
			return
		}

		fmt.Printf("Respuesta: %s\n", string(buffer[0:n]))

	}
}
