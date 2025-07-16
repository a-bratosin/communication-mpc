# Codul pentru laptop

# aici am făcut ca cele două componente să lucreze prin TCP (asigură transmiterea corectă a datelor, dar e mai încet)
# alternativa ar fi UDP (mai rapid, dar nu asigură integritatea). Având în vedere că laptopul și placa sunt în aceeași cameră, am zis că nu contează atât de mult viteza protocolului
# dar pot schimba să meargă pe UDP dacă e prea încet


# laptopul o să fie clientul (se conectează la server), iar placa o să fie serverul de TCP (așteaptă conexiune de la client)


import common
import socket
import sys


def init_connection(host_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host_ip, port))
    except:
        print("Nu s-a putut realiza conexiunea la placă!")
        sys.exit(0)

    return sock






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


init_connection(HOST_IP, HOST_PORT)


