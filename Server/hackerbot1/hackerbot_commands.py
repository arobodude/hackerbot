import serial
import threading

class SerialDevice:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMC0', 230400)
        self.read_thread = threading.Thread(target=self.read_serial)
        self.read_thread.daemon = True
        self.read_thread.start()

    def send_command(self, command):
        command = command + "\n"
        self.ser.write(command.encode('utf-8') + b'\r')

    def read_serial(self):
        while True:
            if self.ser.in_waiting > 0:
                response = self.serial_con.readline().decode('utf8').strip()
                print(response)

    def disconnect(self):
        self.ser.close()


def ping_command():
    send_command("PING")

def send_command(command):
    device = SerialDevice()
    device.send_command(command)
    device.disconnect()
