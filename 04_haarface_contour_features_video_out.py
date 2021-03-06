import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

# Sets camera to 320x240
ret = cap.set(3,320)
ret = cap.set(4,240)

# Output video
out = cv2.VideoWriter('output.mov',cv2.cv.CV_FOURCC('m','p','4','v'), 20.0, (320,240))

# Output data
out_file = open('output.txt', 'w')
frame_counter = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
      # Face ROI
      img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
      roi_gray = gray[y:y+h, x:x+w]
      roi_color = frame[y:y+h, x:x+w]
      
      # Convert to binary by threshold
      ret,thresh = cv2.threshold(roi_gray,0,255,0,1)
      # Find contours
      contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      
      if len(contours) > 0:
        # By hierarchy, we get just the first (bigger) contour
        cnt = contours[0]
        img = cv2.drawContours(roi_color, [cnt], -1, (0,255,0), 3)

        # Image moments
        #M = cv2.moments(cnt)

        #if M['m00'] > 0:
        #centroid_x = int(M['m10']/M['m00'])
        #centroid_y = int(M['m01']/M['m00'])
        # Some features (area, perimeter, angle)
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt,True)
        #angle = '?'
        #if len(cnt) >= 5:
        #  (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
        # Create a mask to make it possible to find its mean value of color
        #mask = np.zeros(roi_gray.shape,np.uint8)
        #pixelpoints = np.transpose(np.nonzero(mask))
        #mean_val = cv2.mean(roi_gray, mask = mask)
        #print 'Centroid: (%s,%s). Area: %d. Perimeter: %d.' % (centroid_x, centroid_y, area, perimeter)
        #print [frame_counter, area, perimeter, x, y]
        out_file.write("%s\n" % [frame_counter, area, perimeter, x, y])
    # Write to file
    #if ret==True:
    # Write the flipped frame
    out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame_counter += 1

# When everything done, release the capture
cap.release()
out.release()
out_file.close()
cv2.destroyAllWindows()

