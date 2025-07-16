# Codul pentru laptop

# aici am făcut ca cele două componente să lucreze prin TCP (asigură transmiterea corectă a datelor, dar e mai încet)
# alternativa ar fi UDP (mai rapid, dar nu asigură integritatea). Având în vedere că laptopul și placa sunt în aceeași cameră, am zis că nu contează atât de mult viteza protocolului
# dar pot schimba să meargă pe UDP dacă e prea încet


# laptopul o să fie clientul (se conectează la server), iar placa o să fie serverul de TCP (așteaptă conexiune de la client)



from common import *
import socket
import sys
import regex

def init_connection(host_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host_ip, port))
    except:
        print("Nu s-a putut realiza conexiunea la placă!")
        sys.exit(0)

    return sock

def send_command(sock, data):
    sock.send(data)

# GPIO init

# TCP socket init

num_args = len(sys.argv)
if(num_args != 3):
    print("format: python " + sys.argv[0] + " BOARD_IP PORT")
    sys.exit(0)

HOST_IP = sys.argv[1]
HOST_PORT = sys.argv[2]

#cam hacky, dar așa o să fie portul luat ca int dacă se poate
try:
    HOST_PORT = int(HOST_PORT)
except:
    print("Port invalid!")
    sys.exit(0)

print("test")
HOST_PORT = int(HOST_PORT)


sock = init_connection(HOST_IP, HOST_PORT)


# aici ar veni partea de generare de traiectorie


while True:
    # aici e placeholder, momentan nu fac nimica cu data
    sensor_data = sock.recv(SENSOR_BUF_SIZE)
    print(sensor_data)

    data: CommandDataArray
    
    num_commands = input("enter number of commands")
    data.commandNumber = int(num_commands)

    data.dt = float("enter command interval")
    for i in range(num_commands):
        
        command_str= input("insert command at moment " + i)

        parts = command_str.strip().split()
        if len(parts) != 4:
            print("Invalid command format. Please enter: [float] [int] [float] [int]")
            continue
        try:
            float1 = float(parts[0])
            int1 = int(parts[1])
            float2 = float(parts[2])
            int2 = int(parts[3])
            
            command = CommandData(leftMotorTuration=float1, leftMotorOrientation=int1, rightMotorTuration=float2, rightMotorOrientation=int2)
            data.commandArray[i] = command

        except ValueError:
            print("Invalid values. Please enter: [float] [int] [float] [int]")
            i-=1
            continue
    

    send_command(sock, data)        

    # clientul (laptopul), așteaptă date de la senzori, face calculele, trimite la server (placă) comanda, rinse and repeat


#print("success")
