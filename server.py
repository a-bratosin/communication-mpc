from common import *
import socket
from time import sleep
import netifaces as ni
from gpiozero import PWMOutputDevice, OutputDevice
import pickle

SERVER_PORT = 5010
WIFI_INTERFACE = 'wlan0'

# Pini: 2 PWM + 4 direcție
MOTOR_PINS = {
    'leftPwm': 13,        # ENA
    'rightPwm': 16,       # ENB
    'leftForward': 17,    # IN1
    'leftBackward': 27,   # IN2
    'rightForward': 23,   # IN3
    'rightBackward': 24   # IN4
}


def init_connection(host_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host_ip, port))
    sock.listen(1)
    conn, addr = sock.accept()
    return sock, conn, addr


# GPIO init
leftPwm = PWMOutputDevice(MOTOR_PINS["leftPwm"])
rightPwm = PWMOutputDevice(MOTOR_PINS["rightPwm"])

leftForward = OutputDevice(MOTOR_PINS["leftForward"])
leftBackward = OutputDevice(MOTOR_PINS["leftBackward"])
rightForward = OutputDevice(MOTOR_PINS["rightForward"])
rightBackward = OutputDevice(MOTOR_PINS["rightBackward"])

# Networking init
ip = ni.ifaddresses(WIFI_INTERFACE)[ni.AF_INET][0]['addr']
print(ip)

sock, conn, addr = init_connection(ip, SERVER_PORT)
print("success")

def set_motor_direction(forward_pin, backward_pin, orientation):
    if orientation == 1:
        forward_pin.on()
        backward_pin.off()
    elif orientation == -1:
        forward_pin.off()
        backward_pin.on()
    else:  # stop / frână
        forward_pin.off()
        backward_pin.off()


try:
    while True:
        sensor_data = "test".encode()
        conn.send(sensor_data)

        encoded_input_data_array = conn.recv(COMMAND_BUF_SIZE)
        input_data_array = pickle.loads(encoded_input_data_array)

        for input_data in input_data_array.commandArray:
            # Setează direcția
            set_motor_direction(leftForward, leftBackward, input_data.leftMotorOrientation)
            set_motor_direction(rightForward, rightBackward, input_data.rightMotorOrientation)

            # Setează viteza
            leftPwm.value = input_data.leftMotorTuration
            rightPwm.value = input_data.rightMotorTuration

            sleep(input_data_array.dt)

except Exception as exception:
    print("exception " + type(exception).__name__ + " raised, shutting down")
    conn.close()

conn.close()


