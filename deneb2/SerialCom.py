import serial
import time
import sys
import glob
from dronekit import connect, VehicleMode


def ConnectSerialDevice(set_connection_port,set_connection_baudrate):
    device = connect(set_connection_port , wait_ready = False , baud = set_connection_baudrate)
    #device.wait_ready(True)
    return device

def CheckAvailableSerial():
    val = {}
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    i = 0
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append((s.portstr))
            for choice in result:
                val[i] = choice
                i+=1

        except (OSError, serial.SerialException):
            pass
    return val
