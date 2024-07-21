import cv2
import time

frames = 5   # Grab 5 images
interval = 7 # Every 7 seconds

frame0 = cv2.VideoCapture(0)
frame0.release()
frame0 = cv2.VideoCapture(0)

for i in range(frames):

   ret0, img0 = frame0.read()
   img1 = img0 #cv2.resize(img0,(1280,720)) # Image comes in at 640x480
   if (frame0):
       cv2.imwrite('./img_'+str(i).zfill(4)+'.jpg',img1)

   time.sleep(interval)

frame0.release()
cv2.destroyAllWindows()
