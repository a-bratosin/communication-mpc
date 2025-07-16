#Codul pentru placă

import common
import socket
import sys
import netifaces as ni

SERVER_PORT = 5010
WIFI_INTERFACE = 'wlan0' # numele interfeței de rețea pe care se conectează placa, necesar pt a afla adresa IP asignată plăcii

def init_connection(host_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host_ip, port))
    sock.listen(1)

    conn, addr = sock.accept()

    return sock, conn, addr





ip = ni.ifaddresses(WIFI_INTERFACE)[ni.AF_INET][0]['addr']
print(ip)
init_connection(ip, SERVER_PORT)

