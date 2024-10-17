import serial
import threading
import time
import os

ser = serial.Serial(
    #port='/devtyACM0',
    port='COM11',
    baudrate=230400,
    timeout=0.1)

def listen_serial():
    while True:
        if ser.in_waiting > 0:
            ser_bytes = ser.readline()
            if ser_bytes:
                message = ser_bytes.decode('utf-8').strip()
                if "55 AA 12" in message:
                    with open("test_data.txt", "a") as f:
                        packet = message[21:-6]
                        packet = packet.replace(" ", "")
                        f.write(f"{packet}")

def send_serial():
    while True:
        user_input = input("?:")
        ser.write(user_input.encode('utf-8') + b'\r')

if __name__ == "__main__":
    ser.flushInput()
    if os.path.isfile("test_data.txt"):
        os.remove("test_data.txt")

    with open("test_data.txt", "w") as f:
        f.write("")

    listener_thread = threading.Thread(target=listen_serial, daemon=True)
    listener_thread.start()
    send_serial()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()



