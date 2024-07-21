import serial

def ping_command():
    send_command("PING")

def send_command(command):
    ser = connect()
    command = command + "\n"
    ser.write(command.encode())
    print(ser.readline().decode('utf-8'))
    disconnect(ser)

def connect():
    ser = serial.Serial('/dev/ttyAMC0', 230400, timeout=1)
    return ser

def disconnect(ser):
    ser.close()