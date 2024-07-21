##############################
# Ian Bernstein
# February 19th, 2024
#
# pip3 install opencv-python
# pip3 install pupil-apriltags
# pip3 install pyserial
#
##############################

import cv2
import time
import serial
from pupil_apriltags import Detector


# Start Serial
#ser = serial.Serial(port='/dev/ttyACM0', baudrate=230400)
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
ser.close()
ser.open()
time.sleep(1)
#ser.write("IDLE,1\r\n".encode())
#time.sleep(1)
#while 1:
#        x = ser.readline()
#        print(x)
#ser.close()

# Start Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, 20)
print(cap.get(cv2.CAP_PROP_FPS))

at_detector = Detector(
   families="tag25h9",
   nthreads=1,
   quad_decimate=1.0,
   quad_sigma=0.0,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

prev_frame_time = 0
new_frame_time = 0

while True:
    success, color_img = cap.read()
    grey_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

    tags = at_detector.detect(grey_img)

    for tag in tags:
        for idx in range(len(tag.corners)):
            cv2.line(color_img, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

        if tag.tag_id == 1:
            tag_text = str(tag.tag_id)
            cv2.putText(color_img, tag_text,
                org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                color=(0, 0, 255))
            cv2.circle(color_img, (int(tag.center[0]), int(tag.center[1])), 5, (0, 0, 255), 2)
            #Face found = 1 X = 50 Y = 50 W = 640 H = 480 W_Min = 40 H_Min = 40 W_Max = 60 H_Max = 60 
            ser.write("Face found = 1 X = ".encode())
            ser.write(str(int(tag.center[0])).encode())
            ser.write(" Y = ".encode())
            ser.write(str(int(tag.center[1])).encode())
            ser.write(" W = 640 H = 480 W_Min = 0 H_Min = 0 W_Max = 640 H_Max = 480\r\n".encode())
            #print("Detection at: ")
            #print(str(int(tag.center[0])))
            #print(str(int(tag.center[1])))
            #time.sleep(0.2)

    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    fps = "FPS: " + str(fps)
    cv2.putText(color_img, fps, (7, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, 2)

    cv2.imshow('Webcam', color_img)
    if cv2.waitKey(1) == ord('q'):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()
