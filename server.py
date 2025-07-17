#Codul pentru placă

from common import *
import socket
from time import sleep
import netifaces as ni
from gpiozero import PWMOutputDevice, OutputDevice
import pickle
SERVER_PORT = 5010
WIFI_INTERFACE = 'wlan0' # numele interfeței de rețea pe care se conectează placa, necesar pt a afla adresa IP asignată plăcii


# astea sunt provizorii, și specifice plăcii pe care testez, și sunt alți pini pt driverul pe care îl folosim
# Pentru placa propriu-zisă, ar veni:
# (pinii ăștia sunt cei pe care i-am găsit în exemplele de cod făcute de Keyestudio)
'''
MOTOR_PINS = {
    'leftCtrl': 2,
    'leftPwm': 5,
    'rightCtrl': 4,
    'rightPwm': 6
}
'''

MOTOR_PINS = {
    'leftCtrl': 17,
    'leftPwm': 27,
    'rightCtrl': 22,
    'rightPwm': 23
}


def init_connection(host_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host_ip, port))
    sock.listen(1)

    conn, addr = sock.accept()

    return sock, conn, addr


# gpio init

leftPwm = PWMOutputDevice(MOTOR_PINS["leftPwm"])
rightPwm = PWMOutputDevice(MOTOR_PINS["rightPwm"])
leftOrientation = OutputDevice(MOTOR_PINS["leftCtrl"])
rightOrientation = OutputDevice(MOTOR_PINS["rightCtrl"])
leftDutyCycle = 0
rightDutyCycle = 0

# networking init

ip = ni.ifaddresses(WIFI_INTERFACE)[ni.AF_INET][0]['addr']
print(ip) 

sock, conn, addr = init_connection(ip, SERVER_PORT)
print("success")


try:
    while True:
        # insert sensing stuff here
        sensor_data = "test".encode()
        conn.send(sensor_data)

        
        encoded_input_data_array = conn.recv(COMMAND_BUF_SIZE)
        input_data_array = pickle.loads(encoded_input_data_array) 
        # pentru fiecare input din array, pornește pinii corespunzători, și menține acea comandă pentru dt secunde/milisecunde
        for input_data in input_data_array.commandArray:

            leftDutyCycle = input_data.leftMotorTuration
            rightDutyCycle = input_data.rightMotorTuration
            
            leftPwm.value = leftDutyCycle
            rightPwm.value = rightDutyCycle

            leftOrientation = input_data.leftMotorOrientation
            rightOrientation = input_data.rightMotorOrientation
            sleep(input_data_array.dt)
except Exception as exception:
    print("exception " + type(exception).__name__ + " raised, shutting down")
    conn.close()



# TODO: bucla în sine
conn.close()


