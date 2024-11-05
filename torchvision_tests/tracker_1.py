#Import the necessary Packages for this software to run
import mediapipe
import cv2
import serial
import time

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
ser.close()
ser.open()
time.sleep(1)

ser.write("DIR,180,180,30\r\n".encode())
currentX = 180
currentY = 180

intX = 0
intY = 0

#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

#Use CV2 Functionality to create a Video stream and add some values
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
     while True:
           ret, frame = cap.read()
           #Unedit the below line if your live feed is produced upsidedown
           #flipped = cv2.flip(frame, flipCode = -1)
           
           #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
           frame1 = cv2.resize(frame, (640, 480))
           
           #Produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
           
           #In case the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                  
                  #Below is Added Code to find and print to the shell the Location X-Y coordinates of Index Finger, Uncomment if desired
                  for point in handsModule.HandLandmark:
                      
                      normalizedLandmark = handLandmarks.landmark[point]
                      pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 640, 480)
                      
                      #Using the Finger Joint Identification Image we know that point 8 represents the tip of the Index Finger
                      if point == 8:
                          print(point)
                          print(pixelCoordinatesLandmark)
                          print(normalizedLandmark)
                          
                          if (pixelCoordinatesLandmark):
                              print(pixelCoordinatesLandmark[0]-320)
                              print(pixelCoordinatesLandmark[1]-240)
                               
                              errorX = (pixelCoordinatesLandmark[0]-320)
                              errorY = (pixelCoordinatesLandmark[1]-240)
                              
                              intX = intX + errorX
                              intY = intY + errorY
                              
                              currentX = 180 - (0.1 * errorX) - (0.01 * intX)
                              currentY = 180 - (0.1 * errorY) - (0.01 * intY)
                              
                              print(currentX)
                              print(currentY)
                              
                              ser.write("DIR,".encode())
                              ser.write(str(currentX).encode())
                              ser.write(",".encode())
                              ser.write(str(currentY).encode())
                              ser.write(",60\r\n".encode())
                              #ser.write(str(int(currentX)).encode())
                              #ser.write(str(int(tag.center[1])).encode())
                              #ser.write(" W = 640 H = 480 W_Min = 0 H_Min = 0 W_Max = 640 H_Max = 480\r\n".encode())
            
           #Below shows the current frame to the desktop 
           cv2.imshow("Frame", frame1);
           key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              break
