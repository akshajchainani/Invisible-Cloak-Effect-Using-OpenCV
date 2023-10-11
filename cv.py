import cv2 
import numpy as np 
import time 

capture_video = cv2.VideoCapture(0) 
     
# Camera takes a second to warm up 
time.sleep(1)  

background = 0 
  
# Capturing the background for some frames 
for i in range(60): 
    return_val, background = capture_video.read() 
    if return_val == False : 
        continue 
  
while True: 
    return_val, frame = capture_video.read() 
    if not return_val : 
        break 
  
    # Converting BGR to HSV for better capture of hues
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    
    # Setting the lower and upper range for red
    lower_red1 = np.array([0, 120, 70])        
    upper_red1 = np.array([10, 255, 255]) 

    lower_red2 = np.array([170, 120, 70])        
    upper_red2 = np.array([180, 255, 255]) 

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1) 
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2) 
  
    mask = mask1 + mask2  # Combine both masks
  
    # Remove noise with Gaussian Blur
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
  
    # Refining the mask using morphological operations
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=2) 
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1) 
  
    # Use contours to find the largest connected component
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        mask = np.zeros_like(mask)
        cv2.drawContours(mask, [largest_contour], 0, 255, -1)
  
    # Final output 
    res1 = cv2.bitwise_and(background, background, mask=mask) 
    res2 = cv2.bitwise_and(frame, frame, mask=~mask)  # Inverted mask
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 
  
    cv2.imshow("MY CLOAK", final_output) 
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

capture_video.release()
cv2.destroyAllWindows()
