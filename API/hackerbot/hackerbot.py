import serial
import threading

class HackerBot:
    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=230400)
        self.read_thread = threading.Thread(target=self.read_serial)
        self.read_thread.daemon = True
        self.read_thread.start()

    def init_command(self):
        self.send_command("INIT")
        return True

    def ping_command(self):
        self.send_command("PING")
        return True

    def dock_command(self):
        self.send_command("DOCK")
        return True

    def goto_command(self, x_coord, y_coord, angle, speed):
        command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
        self.send_command(command)
        return True

    def get_ml_command(self):
        self.send_command("GETML")
        return True

    def send_command(self, command):
        command = command + "\n"
        self.ser.write(command.encode('utf-8') + b'\r')

    def play_audio_file(self, audio_file):
        return True

    def read_serial(self):
        while True:
            if self.ser.in_waiting > 0:
                response = self.serial_con.readline().decode('utf8').strip()
                print(response)

    def disconnect(self):
        self.ser.close()




